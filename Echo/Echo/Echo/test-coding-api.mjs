#!/usr/bin/env node
// 测试 Coding OpenAPI DescribeIssue 接口
// 用法: node test-coding-api.mjs

import { existsSync, readFileSync } from "fs"
import { homedir } from "os"
import { join } from "path"

// 读取 token（从 openclaw .env 或本地 .env）
const envPaths = [
  join(import.meta.dirname, ".env"),
  join(homedir(), ".openclaw", ".env"),
]

let token = ""
for (const envPath of envPaths) {
  if (existsSync(envPath)) {
    const content = readFileSync(envPath, "utf8")
    for (const line of content.split("\n")) {
      const m = line.match(/^CODING_TOKEN=(.+)$/)
      if (m) { token = m[1].trim().replace(/^["']|["']$/g, ""); break }
    }
  }
  if (token) break
}

if (!token) {
  console.error("Missing CODING_TOKEN — add to .env or ~/.openclaw/.env")
  process.exit(1)
}

// 测试两种 URL 格式的解析
const testUrls = [
  "https://mabangerp.coding.net/p/mdc/requirements/issues/56292/detail",
  "https://mabangerp.coding.net/p/wuliu/all/issues/106983",
]

function parseUrl(url) {
  const m = url.match(/\/p\/([^/]+)\/(?:[^/]+\/)?issues\/(\d+)/)
  if (!m) return null
  return { projectName: m[1], issueCode: parseInt(m[2], 10) }
}

for (const url of testUrls) {
  const parsed = parseUrl(url)
  console.log(`\nURL: ${url}`)
  console.log(`解析结果:`, parsed)

  if (!parsed) { console.log("❌ 解析失败"); continue }

  const resp = await fetch("https://mabangerp.coding.net/open-api", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `token ${token}`,
    },
    body: JSON.stringify({
      Action: "DescribeIssue",
      ProjectName: parsed.projectName,
      IssueCode: parsed.issueCode,
      ShowImageOutUrl: false,
    }),
  })

  const data = await resp.json()

  if (data.Response?.Error) {
    console.log(`❌ API错误: [${data.Response.Error.Code}] ${data.Response.Error.Message}`)
    continue
  }

  const issue = data.Response?.Issue
  if (!issue) { console.log("❌ 无数据返回"); continue }

  console.log(`✅ 成功`)
  console.log(`  标题: ${issue.Name}`)
  console.log(`  状态: ${issue.IssueStatusName}`)
  console.log(`  处理人: ${issue.Assignee?.Name ?? "未分配"}`)
  console.log(`  描述(前100字): ${(issue.Description ?? "").slice(0, 100)}`)
}

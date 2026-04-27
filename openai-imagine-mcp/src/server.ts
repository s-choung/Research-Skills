#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { Command } from "commander";
import { ImageGenerator } from "./services/image-generator.js";
import { createGenerateImageTool } from "./tools/generate-image.js";
import { createEditImageTool } from "./tools/edit-image.js";

const program = new Command()
  .option("--apiKey <key>", "OpenAI API key for image generation")
  .allowUnknownOption()
  .parse(process.argv);

const cliOptions = program.opts();
const apiKey = cliOptions.apiKey || process.env.OPENAI_API_KEY;

function createServerInstance() {
  const generator = new ImageGenerator(apiKey);
  const server = new McpServer({
    name: "openai-imagine-mcp",
    version: "0.1.0",
  });

  const generateImageTool = createGenerateImageTool(generator);
  const editImageTool = createEditImageTool(generator);

  server.registerTool(generateImageTool.name, {
    title: "Generate Image",
    description: generateImageTool.description,
    inputSchema: generateImageTool.inputSchema.shape,
    outputSchema: undefined,
  }, generateImageTool.handler);

  server.registerTool(editImageTool.name, {
    title: "Edit Image",
    description: editImageTool.description,
    inputSchema: editImageTool.inputSchema.shape,
    outputSchema: undefined,
  }, editImageTool.handler);

  return server;
}

async function main() {
  const server = createServerInstance();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("OpenAI Imagine MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});

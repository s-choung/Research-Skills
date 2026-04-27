import { z } from "zod";
import type { ImageGenerator } from "../services/image-generator.js";

export function createGenerateImageTool(generator: ImageGenerator) {
  const inputSchema = z.object({
    prompt: z.string().describe("Text description of the image to generate"),
    output_path: z
      .string()
      .optional()
      .describe(
        "Optional ABSOLUTE path where the generated image will be saved. If not provided, returns base64 encoded image data. Example: /Users/username/images/output.png"
      ),
    model: z
      .enum(["gpt-image-2", "gpt-image-1.5", "gpt-image-1", "gpt-image-1-mini"])
      .optional()
      .default("gpt-image-2")
      .describe(
        "Model to use (gpt-image-2: best quality, gpt-image-1.5: balanced, gpt-image-1: standard, gpt-image-1-mini: fast/cheap). Default: gpt-image-2"
      ),
    size: z
      .enum(["1024x1024", "1024x1536", "1536x1024", "auto"])
      .optional()
      .default("1024x1024")
      .describe(
        "Image size (1024x1024: square, 1024x1536: portrait, 1536x1024: landscape, auto: model decides)"
      ),
    quality: z
      .enum(["low", "medium", "high"])
      .optional()
      .default("high")
      .describe("Image quality (default: high)"),
    background: z
      .enum(["transparent", "opaque", "auto"])
      .optional()
      .default("auto")
      .describe(
        "Background style. 'transparent' requires PNG output. (default: auto)"
      ),
    n: z
      .number()
      .int()
      .min(1)
      .max(4)
      .optional()
      .default(1)
      .describe("Number of images to generate (1-4, default: 1)"),
  });

  return {
    name: "generate_image",
    description:
      "Generates an image based on a text prompt using OpenAI gpt-image-1 model.",
    inputSchema,
    async handler(input: z.infer<typeof inputSchema>) {
      try {
        const result = await generator.generateImage(
          input.prompt,
          input.output_path,
          input.model,
          input.quality,
          input.size,
          input.background,
          input.n
        );

        if (input.output_path) {
          return {
            content: [
              {
                type: "text" as const,
                text: `Image successfully generated and saved to: ${result}`,
              },
            ],
          };
        }
        return {
          content: [
            {
              type: "text" as const,
              text: `Image successfully generated. Base64 data:\n${result}`,
            },
          ],
        };
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : String(error);
        return {
          content: [
            {
              type: "text" as const,
              text: `Error generating image: ${errorMessage}`,
            },
          ],
          isError: true,
        };
      }
    },
  };
}

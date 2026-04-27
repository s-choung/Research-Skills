import { z } from "zod";
import type { ImageGenerator } from "../services/image-generator.js";

export function createEditImageTool(generator: ImageGenerator) {
  const inputSchema = z.object({
    path: z
      .string()
      .optional()
      .describe(
        "ABSOLUTE path to the image to edit. Either 'path' or 'image_base64' must be provided."
      ),
    image_base64: z
      .string()
      .optional()
      .describe(
        "Base64 encoded image data to edit. Either 'path' or 'image_base64' must be provided."
      ),
    mime_type: z
      .string()
      .optional()
      .describe(
        "MIME type of the base64 image (e.g., 'image/png'). Required when using 'image_base64'."
      ),
    prompt: z.string().describe("Text description of the edits to make"),
    model: z
      .enum(["gpt-image-2", "gpt-image-1.5", "gpt-image-1", "gpt-image-1-mini"])
      .optional()
      .default("gpt-image-2")
      .describe(
        "Model to use (gpt-image-2: best quality, gpt-image-1.5: balanced, gpt-image-1: standard, gpt-image-1-mini: fast/cheap). Default: gpt-image-2"
      ),
    output_path: z
      .string()
      .optional()
      .describe(
        "Optional ABSOLUTE path where the edited image will be saved. If not provided and 'path' is used, overwrites the input file."
      ),
    mask_path: z
      .string()
      .optional()
      .describe(
        "Optional ABSOLUTE path to a mask image. Transparent areas indicate where to edit."
      ),
    size: z
      .enum(["1024x1024", "1024x1536", "1536x1024", "auto"])
      .optional()
      .default("1024x1024")
      .describe("Output image size (default: 1024x1024)"),
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
    name: "edit_image",
    description:
      "Edits an existing image based on a text prompt using OpenAI gpt-image-1 model. Supports optional mask for targeted inpainting.",
    inputSchema,
    async handler(input: z.infer<typeof inputSchema>) {
      try {
        if (!input.path && !input.image_base64) {
          throw new Error("Either 'path' or 'image_base64' must be provided");
        }
        if (input.path && input.image_base64) {
          throw new Error(
            "Cannot provide both 'path' and 'image_base64'. Choose one."
          );
        }
        if (input.image_base64 && !input.mime_type) {
          throw new Error(
            "'mime_type' is required when using 'image_base64'"
          );
        }

        let imageInput: string | { base64: string; mimeType: string };
        let defaultOutputPath: string | undefined;

        if (input.path) {
          imageInput = input.path;
          defaultOutputPath = input.output_path || input.path;
        } else {
          imageInput = {
            base64: input.image_base64!,
            mimeType: input.mime_type!,
          };
          defaultOutputPath = input.output_path;
        }

        const result = await generator.editImage(
          imageInput,
          input.prompt,
          defaultOutputPath,
          input.model,
          input.mask_path,
          input.size,
          input.n
        );

        if (defaultOutputPath) {
          return {
            content: [
              {
                type: "text" as const,
                text: `Image successfully edited and saved to: ${result}`,
              },
            ],
          };
        }
        return {
          content: [
            {
              type: "text" as const,
              text: `Image successfully edited. Base64 data:\n${result}`,
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
              text: `Error editing image: ${errorMessage}`,
            },
          ],
          isError: true,
        };
      }
    },
  };
}

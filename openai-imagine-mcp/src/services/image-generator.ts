import OpenAI, { toFile } from "openai";
import * as fs from "node:fs";
import * as path from "node:path";

export type ImageSize =
  | "1024x1024"
  | "1024x1536"
  | "1536x1024"
  | "auto";

export type ImageQuality = "low" | "medium" | "high";

export type ImageModel =
  | "gpt-image-2"
  | "gpt-image-1.5"
  | "gpt-image-1"
  | "gpt-image-1-mini";

export class ImageGenerator {
  private client: OpenAI;

  constructor(apiKey?: string) {
    const key = apiKey || process.env.OPENAI_API_KEY;
    if (!key) {
      throw new Error(
        "OpenAI API key is required. Set OPENAI_API_KEY environment variable or provide it in constructor."
      );
    }
    this.client = new OpenAI({ apiKey: key });
  }

  async generateImage(
    prompt: string,
    outputPath?: string,
    model: ImageModel = "gpt-image-2",
    quality: ImageQuality = "high",
    size: ImageSize = "1024x1024",
    background: "transparent" | "opaque" | "auto" = "auto",
    n: number = 1
  ): Promise<string> {
    const response = await this.client.images.generate({
      model,
      prompt,
      quality,
      size,
      background,
      n,
    });

    if (!response.data || response.data.length === 0) {
      throw new Error("No image data returned in the response");
    }

    const imageData = response.data[0].b64_json;
    if (!imageData) {
      throw new Error("No base64 image data in the response");
    }

    if (!outputPath) {
      return imageData;
    }

    const buffer = Buffer.from(imageData, "base64");
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(outputPath, buffer);
    return outputPath;
  }

  async editImage(
    imageInput: string | { base64: string; mimeType: string },
    prompt: string,
    outputPath?: string,
    model: ImageModel = "gpt-image-2",
    maskPath?: string,
    size: ImageSize = "1024x1024",
    n: number = 1
  ): Promise<string> {
    let imageFile: Parameters<typeof this.client.images.edit>[0]["image"];

    if (typeof imageInput === "string") {
      const imageBuffer = fs.readFileSync(imageInput);
      const mimeType = this.getMimeType(imageInput);
      const fileName = path.basename(imageInput);
      imageFile = await toFile(imageBuffer, fileName, { type: mimeType });
    } else {
      const buffer = Buffer.from(imageInput.base64, "base64");
      imageFile = await toFile(buffer, "input.png", {
        type: imageInput.mimeType,
      });
    }

    const editParams: Parameters<typeof this.client.images.edit>[0] = {
      model,
      image: imageFile,
      prompt,
      size,
      n,
    };

    if (maskPath) {
      const maskBuffer = fs.readFileSync(maskPath);
      const maskMime = this.getMimeType(maskPath);
      editParams.mask = await toFile(maskBuffer, path.basename(maskPath), {
        type: maskMime,
      });
    }

    const response = await this.client.images.edit(editParams);

    if (!response.data || response.data.length === 0) {
      throw new Error("No image data returned in the response");
    }

    const imageData = response.data[0].b64_json;
    if (!imageData) {
      throw new Error("No base64 image data in the response");
    }

    if (!outputPath) {
      return imageData;
    }

    const buffer = Buffer.from(imageData, "base64");
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(outputPath, buffer);
    return outputPath;
  }

  private getMimeType(filePath: string): string {
    const ext = path.extname(filePath).toLowerCase();
    const mimeTypes: Record<string, string> = {
      ".jpg": "image/jpeg",
      ".jpeg": "image/jpeg",
      ".png": "image/png",
      ".gif": "image/gif",
      ".webp": "image/webp",
    };
    return mimeTypes[ext] || "image/png";
  }
}

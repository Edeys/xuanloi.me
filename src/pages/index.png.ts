import type { APIRoute } from "astro";
import { SITE } from "@/config";
import { generateOgImageForSite } from "@/utils/generateOgImages";

export const GET: APIRoute = async () => {
  if (!SITE.dynamicOgImage) {
    return new Response(null, { status: 404, statusText: "Not found" });
  }

  const png = await generateOgImageForSite();
  return new Response(new Uint8Array(png), {
    headers: { "Content-Type": "image/png" },
  });
};

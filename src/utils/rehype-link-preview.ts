import { visit } from "unist-util-visit";
import axios from "axios";
import * as cheerio from "cheerio";
import fs from "node:fs";
import path from "node:path";

const CACHE_FILE = path.resolve("src/data/link-preview-cache.json");

function loadCache() {
  if (fs.existsSync(CACHE_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(CACHE_FILE, "utf-8"));
    } catch {
      return {};
    }
  }
  return {};
}

function saveCache(cache: Record<string, any>) {
  fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), "utf-8");
}

async function fetchMetadata(url: string) {
  try {
    const { data } = await axios.get(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
      },
      timeout: 5000,
    });
    const $ = cheerio.load(data);

    const title =
      $('meta[property="og:title"]').attr("content") ||
      $("title").text() ||
      url;
    const description =
      $('meta[property="og:description"]').attr("content") ||
      $('meta[name="description"]').attr("content") ||
      "";
    const image =
      $('meta[property="og:image"]').attr("content") ||
      $('meta[property="twitter:image"]').attr("content") ||
      "";
    const siteName =
      $('meta[property="og:site_name"]').attr("content") ||
      new URL(url).hostname;

    return { title, description, image, siteName, url };
  } catch (error: any) {
    console.error(`Failed to fetch metadata for ${url}:`, error.message);
    return null;
  }
}

export function rehypeLinkPreview() {
  const cache = loadCache();
  let cacheUpdated = false;

  return async (tree: any) => {
    const promises: Promise<void>[] = [];

    visit(tree, "element", (node: any, index: number | undefined, parent: any) => {
      // Look for standalone link: <p><a>URL</a></p>
      if (
        node.tagName === "p" &&
        node.children.length === 1 &&
        node.children[0].tagName === "a"
      ) {
        const linkNode = node.children[0];
        const url = linkNode.properties.href;
        const text = linkNode.children[0]?.value;

        // Only convert if the link is the only text in the paragraph
        if (url && (text === url || !text) && index !== undefined) {
          promises.push(
            (async () => {
              let metadata = cache[url];
              if (!metadata) {
                metadata = await fetchMetadata(url);
                if (metadata) {
                  cache[url] = metadata;
                  cacheUpdated = true;
                }
              }

              if (metadata) {
                // Replace the paragraph with a Link Card
                const cardHtml = `
                  <div class="link-card-container my-8">
                    <a href="${url}" target="_blank" rel="noopener noreferrer" class="link-card group">
                      <div class="link-card-content">
                        <div class="link-card-title group-hover:text-accent">${metadata.title}</div>
                        <div class="link-card-description">${metadata.description}</div>
                        <div class="link-card-site">${metadata.siteName}</div>
                      </div>
                      ${
                        metadata.image
                          ? `<div class="link-card-image" style="background-image: url('${metadata.image}')"></div>`
                          : ""
                      }
                    </a>
                  </div>
                `.trim();

                // Convert HTML to HAST (using a simple approach for rehype)
                parent.children[index] = {
                  type: "element",
                  tagName: "div",
                  properties: { className: ["link-card-wrapper"] },
                  children: [
                    {
                      type: "raw",
                      value: cardHtml,
                    },
                  ],
                };
              }
            })()
          );
        }
      }
    });

    await Promise.all(promises);
    if (cacheUpdated) {
      saveCache(cache);
    }
  };
}

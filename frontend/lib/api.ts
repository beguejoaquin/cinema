import { error } from "console";

export async function fetchProducts({
  client = false,
}: { client?: boolean } = {}) {
  // In dev environment use different urls to fetch from client and server.
  const API_URL =
    process.env.DEV && client
      ? process.env.SERVER_API_URL
      : process.env.NEXT_PUBLIC_API_URL;

  const res = await fetch(`${API_URL}/products/`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch products ${res.status}`);
  }
  return res.json();
}

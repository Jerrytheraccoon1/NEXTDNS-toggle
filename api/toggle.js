export const config = { runtime: 'edge' };

export default async function handler(req) {
  const NEXTDNS_PROFILE_ID = process.env.NEXTDNS_PROFILE_ID;
  const NEXTDNS_API_KEY = process.env.NEXTDNS_API_KEY;
  const DOMAIN = "ppq.apple.com";

  const url = `https://api.nextdns.io/profiles/${NEXTDNS_PROFILE_ID}/denylist`;
  const headers = { "X-Api-Key": NEXTDNS_API_KEY, "Content-Type": "application/json" };

  try {
    // 1. Check current status
    const response = await fetch(url, { headers });
    const data = await response.json();
    
    const exists = data.data.find(item => item.id === DOMAIN);

    if (exists) {
      // 2. If it exists, DELETE it (Turn OFF blocking)
      await fetch(`${url}/${DOMAIN}`, { method: 'DELETE', headers });
      return new Response(`UNBLOCKED: ${DOMAIN}`);
    } else {
      // 3. If it doesn't exist, POST it (Turn ON blocking)
      await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify({ id: DOMAIN, active: true })
      });
      return new Response(`BLOCKED: ${DOMAIN}`);
    }
  } catch (err) {
    return new Response(`Error: ${err.message}`, { status: 500 });
  }
}

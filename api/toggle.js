export const config = { runtime: 'edge' };

export default async function handler(req) {
  // PASTE YOUR ACTUAL VALUES HERE
  const NEXTDNS_PROFILE_ID = "d6ddb9";
  const NEXTDNS_API_KEY = "65cfb3f31b90b2e9b429422f8781660a1a2a08b9";
  const DOMAIN = "ppq.apple.com";

  const url = `https://api.nextdns.io/profiles/${NEXTDNS_PROFILE_ID}/denylist`;
  const headers = { 
    "X-Api-Key": NEXTDNS_API_KEY, 
    "Content-Type": "application/json" 
  };

  try {
    const response = await fetch(url, { headers });
    const data = await response.json();
    
    // Check if the domain is currently in the list
    const exists = data.data && data.data.find(item => item.id === DOMAIN);

    if (exists) {
      // It's there, so DELETE it (Toggle OFF)
      await fetch(`${url}/${DOMAIN}`, { method: 'DELETE', headers });
      return new Response(`OFF: ${DOMAIN} is now allowed`);
    } else {
      // It's not there, so POST it (Toggle ON)
      await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify({ id: DOMAIN, active: true })
      });
      return new Response(`ON: ${DOMAIN} is now blocked`);
    }
  } catch (err) {
    return new Response(`Fail: ${err.message}`, { status: 500 });
  }
}

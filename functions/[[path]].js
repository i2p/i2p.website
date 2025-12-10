// Cloudflare Pages Function for OS Detection
// Injects data-detected-os attribute on <html> tag for download pages

function detectOS(userAgent) {
  if (!userAgent) return null;
  const ua = userAgent.toLowerCase();

  // Order matters - check more specific patterns first
  if (ua.includes('android')) return 'android';
  if (ua.includes('iphone') || ua.includes('ipad') || ua.includes('ipod')) return null; // No iOS version
  if (ua.includes('windows')) return 'windows';
  if (ua.includes('macintosh') || ua.includes('mac os')) return 'mac';
  if (ua.includes('linux') || ua.includes('x11')) return 'linux';
  if (ua.includes('freebsd') || ua.includes('openbsd') || ua.includes('netbsd')) return 'linux'; // BSD uses same JAR

  return null;
}

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);

  // Only process download pages (all 13 languages)
  if (!/^\/(en|es|ko|zh|ru|cs|de|fr|tr|vi|hi|ar|pt)\/downloads\/?$/.test(url.pathname)) {
    return next();
  }

  const userAgent = request.headers.get('User-Agent');
  const detectedOS = detectOS(userAgent);

  // No OS detected = return unmodified (no recommendation shown)
  if (!detectedOS) {
    return next();
  }

  const response = await next();
  const contentType = response.headers.get('Content-Type');

  if (!contentType || !contentType.includes('text/html')) {
    return response;
  }

  // Inject data attribute on <html> tag
  const html = await response.text();
  const modified = html.replace(/<html([^>]*)>/i, `<html$1 data-detected-os="${detectedOS}">`);

  return new Response(modified, {
    status: response.status,
    headers: response.headers
  });
}

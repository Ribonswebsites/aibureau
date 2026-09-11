from datetime import date
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
BASE = 'https://ailens.online'

# Use a concise, descriptive title instead of a keyword-stuffed list of model names.
index = ROOT / 'index.html'
html = index.read_text(encoding='utf-8')
html = re.sub(r'<title>.*?</title>', '<title>AILens | AI Models, Tools, Companies &amp; Comparisons</title>', html, count=1, flags=re.S | re.I)
html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="AILens is an independent AI information and comparison site covering models, companies, tools, pricing, benchmarks, news, and practical guides. Compare AI products by capability, cost, access, and use case.">', html, count=1, flags=re.I)
html = re.sub(r'<meta name="keywords" content="[^"]*">', '<meta name="keywords" content="AI models, AI tools, AI companies, AI comparisons, AI benchmarks, AI pricing, AI news, artificial intelligence guides">', html, count=1, flags=re.I)
html = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="AILens | AI Models, Tools, Companies &amp; Comparisons">', html, count=1, flags=re.I)
html = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="Independent AI information and comparisons covering models, companies, tools, pricing, benchmarks, news, and practical guides.">', html, count=1, flags=re.I)
html = re.sub(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="AILens | AI Models, Tools, Companies &amp; Comparisons">', html, count=1, flags=re.I)
html = re.sub(r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="Compare AI models, tools, companies, pricing, benchmarks, news, and practical use cases with AILens.">', html, count=1, flags=re.I)
# Keep site-name signals consistent with the visible AILens brand.
html = html.replace('AILens — World\'s #1 AI Intelligence Directory', 'AILens — AI Models, Tools & Comparisons')
html = html.replace('AILens 2026 — #1 AI Directory: Claude Fable 5.1, Opus 5, Grok 4.6, GPT-5.3-Codex, Grok Bot', 'AILens | AI Models, Tools, Companies & Comparisons')
if '<link rel="sitemap"' not in html.lower():
    html = html.replace('</head>', '<link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">\n</head>', 1)
index.write_text(html, encoding='utf-8')

# Keep all substantive public information and comparison pages in the sitemap; omit legal-only pages.
public = [
    'index.html', 'ai.html', 'ai-models.html', 'ai-companies.html', 'ai-news.html', 'ai-videos.html',
    'free-ai-tools.html', 'learn-ai.html', 'claude.html', 'codex.html', 'companies.html', 'founders.html',
    'imgai.html', 'llms.html', 'rankings.html', 'videoai.html', 'voice.html', 'china-ai.html',
    'uncensored-ai.html', 'uncensored-ai-video.html', 'editorial-policy.html'
]
changefreq = {'index.html': 'daily', 'ai-news.html': 'daily', 'editorial-policy.html': 'yearly'}
priority = {'index.html': '1.0', 'ai.html': '0.9', 'ai-models.html': '0.9', 'ai-companies.html': '0.9', 'ai-news.html': '0.9', 'uncensored-ai.html': '0.8', 'uncensored-ai-video.html': '0.8'}
urlset = ET.Element('urlset', {'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
for filename in public:
    if not (ROOT / filename).exists():
        continue
    url = BASE + ('/' if filename == 'index.html' else '/' + filename)
    node = ET.SubElement(urlset, 'url')
    ET.SubElement(node, 'loc').text = url
    ET.SubElement(node, 'lastmod').text = TODAY
    ET.SubElement(node, 'changefreq').text = changefreq.get(filename, 'weekly')
    ET.SubElement(node, 'priority').text = priority.get(filename, '0.75')
ET.indent(urlset, space='  ')
(ROOT / 'sitemap.xml').write_text(ET.tostring(urlset, encoding='unicode', xml_declaration=True) + '\n', encoding='utf-8')

robots = '''# AILens robots.txt
User-agent: *
Allow: /
Disallow: /brand-assets/
Disallow: /brand-assets.zip
Disallow: /assets-manifest.tsv

Sitemap: https://ailens.online/sitemap.xml
'''
(ROOT / 'robots.txt').write_text(robots, encoding='utf-8')
print(f'Updated AILens homepage metadata and rebuilt sitemap with {len(list(urlset))} public information pages.')

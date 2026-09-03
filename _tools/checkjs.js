const fs = require('fs')
const html = fs.readFileSync('index.html', 'utf8')
const m = html.match(/<script>([\s\S]*?)<\/script>/g) || []
console.log('script blocks:', m.length)
m.forEach((block, i) => {
  const code = block.replace(/^<script>/, '').replace(/<\/script>$/, '')
  fs.writeFileSync('_tools/_s' + i + '.js', code)
  try {
    new Function(code)
    console.log('block', i, 'OK  lines=', code.split('\n').length)
  } catch (e) {
    console.log('block', i, 'ERROR:', e.message)
  }
})

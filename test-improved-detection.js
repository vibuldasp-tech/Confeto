// Test improved section detection with actual HTML from document
const sampleHtml = `<p>Suspicious Activity Report (SAR)</p><h1>1. REPORTING FINANCIAL INSTITUTION</h1><p>Institution Name: Example National Bank</p><p>Address: 123 Financial Plaza</p><h1>2. SUSPECT INFORMATION</h1><p>Subject Name: Jane Doe</p><h1>3. SUSPICIOUS ACTIVITY DESCRIPTION</h1><p>Over a period of two weeks...</p><h1>4. BACKGROUND AND ACCOUNT HISTORY</h1><p>Account Opening Date: January 10, 2023</p><h1>5. INVESTIGATION AND ACTIONS TAKEN</h1><p>Internal Review...</p><h1>6. COMPLIANCE OFFICER REVIEW AND DETERMINATION</h1><p>Reviewed By: Sarah Johnson</p><h1>7. FINANCIAL DETAILS</h1><p>Total Amount: $250,000</p><h1>8. ADDITIONAL INFORMATION</h1><p>Law enforcement has not been contacted...</p>`;

function detectSections(html) {
  const sections = [];
  
  const elementRegex = /<(h[1-6]|p)[^>]*>(.*?)<\/\1>/gi;
  const elements = [];
  let match;
  
  while ((match = elementRegex.exec(html)) !== null) {
    const tagName = match[1].toLowerCase();
    const content = match[2].trim();
    elements.push({ tag: tagName, content: content });
  }
  
  let currentSection = null;
  let sectionId = 0;
  
  for (let i = 0; i < elements.length; i++) {
    const element = elements[i];
    const plainText = element.content.replace(/<[^>]*>/g, '').trim();
    
    if (!plainText) continue;
    
    const isHeadingTag = /^h[1-6]$/.test(element.tag);
    
    const isShort = plainText.length < 100;
    const hasNumbering = /^(\d+\.|\d+\.\d+|\[?\d+\]?)/.test(plainText);
    const isAllCaps = plainText === plainText.toUpperCase() && plainText.length > 2 && /[A-Z]/.test(plainText);
    const hasStrongTag = /<strong>/i.test(element.content) || /<b>/i.test(element.content);
    
    const isHeading = isHeadingTag || (isShort && hasStrongTag && (hasNumbering || isAllCaps));
    
    if (isHeading) {
      if (currentSection) {
        sections.push(currentSection);
      }
      sectionId++;
      currentSection = {
        id: sectionId,
        title: plainText.substring(0, 80),
        content: ''
      };
    } else if (currentSection) {
      currentSection.content += element.content + '\n';
    } else {
      sectionId++;
      currentSection = {
        id: sectionId,
        title: plainText.substring(0, 80),
        content: ''
      };
    }
  }
  
  if (currentSection) {
    sections.push(currentSection);
  }
  
  if (sections.length === 0) {
    sections.push({
      id: 1,
      title: 'Document Content',
      content: html
    });
  }
  
  return sections;
}

console.log('Testing improved section detection with actual HTML...\n');
const sections = detectSections(sampleHtml);

console.log(`Detected ${sections.length} sections:\n`);
sections.forEach(section => {
  console.log(`Section ${section.id}: "${section.title}"`);
  console.log(`Content: ${section.content.substring(0, 50).replace(/\n/g, ' ')}...`);
  console.log('---');
});

console.log(`\n✓ Successfully detected ${sections.length} sections from heading tags`);

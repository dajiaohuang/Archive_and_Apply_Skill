const languageContent = {
  zh: {
    title: 'Archive & Apply — 让每个 claim 回到来源',
    description: 'Archive & Apply：把经历证据转化为可追溯、可核验的简历、投递、面试与学术申请材料。',
    ogDescription: 'Source-first 的 Codex skill：从经历证据派生目标材料，并保留验证链路。',
    current: '中',
    other: 'EN',
    toggleLabel: 'Switch to English',
    copied: '已复制',
    copy: '复制命令',
  },
  en: {
    title: 'Archive & Apply — Make every claim trace back',
    description: 'Archive & Apply turns experience evidence into traceable resumes, applications, interview packs, and academic materials.',
    ogDescription: 'A source-first Codex skill that derives targeted materials from evidence while preserving their validation chain.',
    current: 'EN',
    other: '中',
    toggleLabel: '切换为中文',
    copied: 'Copied',
    copy: 'Copy command',
  },
};

const lineageContent = {
  source: {
    zh: {
      index: 'STEP 01 / INPUT',
      title: '保留原貌，再开始判断。',
      copy: '仓库、笔记、PDF、JD 与项目 Prompt 先作为来源被读取；原文和后续分析不会混写。',
      list: ['记录来源路径或 URL', '保存抓取日期与原始状态', '不从文件存在推断作者或贡献'],
    },
    en: {
      index: 'STEP 01 / INPUT',
      title: 'Preserve first. Interpret second.',
      copy: 'Repositories, notes, PDFs, JDs, and program prompts enter as sources. Original material stays separate from later analysis.',
      list: ['Record the source path or URL', 'Preserve capture date and original status', 'Never infer authorship from a file alone'],
    },
  },
  record: {
    zh: {
      index: 'STEP 02 / CANONICAL RECORD',
      title: '事实进入唯一的 canonical 层。',
      copy: '经历、项目和论文条目保存 provenance、日期、结果、贡献边界与未知项。重复材料先去重，不制造平行事实。',
      list: ['区分 verified / user-reported / inferred', '事实变化先更新 source entry', '保留 led、co-built、contributed 等边界'],
    },
    en: {
      index: 'STEP 02 / CANONICAL RECORD',
      title: 'Facts enter one canonical layer.',
      copy: 'Experience, project, and publication entries preserve provenance, dates, outcomes, contribution boundaries, and unknowns without parallel sources of truth.',
      list: ['Separate verified, user-reported, and inferred', 'Update source entries before derivatives', 'Preserve led, co-built, and contributed boundaries'],
    },
  },
  map: {
    zh: {
      index: 'STEP 03 / EVIDENCE MAP',
      title: '先知道目标在判断什么。',
      copy: '把 JD 或项目 Prompt 拆成要求、约束和读者决策，再把每项映射到来源；没有证据的地方明确标记为 gap。',
      list: ['原始要求与分析分开保存', '记录 must-have、preferred 与约束', 'evidence gap 永远不会变成 claim'],
    },
    en: {
      index: 'STEP 03 / EVIDENCE MAP',
      title: 'Know what the target must decide.',
      copy: 'Break a JD or program prompt into requirements, constraints, and reader decisions. Map each one to a source and mark unsupported areas as gaps.',
      list: ['Keep raw requirements separate from analysis', 'Record must-haves, preferences, and constraints', 'An evidence gap never becomes a claim'],
    },
  },
  artifact: {
    zh: {
      index: 'STEP 04 / DERIVATIVE',
      title: '只生成当前目标需要的材料。',
      copy: '简历、面试答案、SOP 或投递记录从映射中派生。只改措辞或选择时，不反向污染事实层。',
      list: ['按真实读者路径安排信息', '每份材料回答自己的 Prompt', '不做只替换名称的伪定制'],
    },
    en: {
      index: 'STEP 04 / DERIVATIVE',
      title: 'Build only what the target needs.',
      copy: 'Resumes, interview answers, statements, and application records derive from the map. Wording and selection changes do not rewrite the factual layer.',
      list: ['Order information for the real reader path', 'Make every document answer its own prompt', 'Never customize by changing names alone'],
    },
  },
  verify: {
    zh: {
      index: 'STEP 05 / VERIFICATION',
      title: 'claim、状态与版式分别核验。',
      copy: '内容检查追溯性与贡献边界；状态检查事件证据；TeX/PDF 检查页数、断页、边界、字体、链接和文本提取。',
      list: ['每个 claim 能经得起面试追问', '准备材料不等于已经投递', '自动诊断后仍逐页检查 PNG'],
    },
    en: {
      index: 'STEP 05 / VERIFICATION',
      title: 'Verify claims, status, and layout separately.',
      copy: 'Content checks traceability and contribution scope; status checks event evidence; TeX/PDF checks pages, breaks, bounds, fonts, links, and extraction.',
      list: ['Every claim survives interview follow-up', 'Prepared never means submitted', 'Inspect every rendered PNG after automation'],
    },
  },
};

const languageToggle = document.querySelector('[data-language-toggle]');
const languageCurrent = document.querySelector('[data-language-current]');
const languageOther = document.querySelector('[data-language-other]');
const copyLabel = document.querySelector('[data-copy-label]');
let activeLineage = 'source';

function applyLineage(step, language) {
  const content = lineageContent[step][language];
  document.querySelector('[data-detail-index]').textContent = content.index;
  document.querySelector('[data-detail-title]').textContent = content.title;
  document.querySelector('[data-detail-copy]').textContent = content.copy;
  const list = document.querySelector('[data-detail-list]');
  list.replaceChildren(...content.list.map((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    return li;
  }));
}

function applyLanguage(language) {
  const content = languageContent[language];
  document.documentElement.dataset.lang = language;
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
  document.title = content.title;
  document.querySelector('meta[name="description"]').content = content.description;
  document.querySelector('meta[property="og:title"]').content = content.title;
  document.querySelector('meta[property="og:description"]').content = content.ogDescription;

  document.querySelectorAll('[data-zh][data-en]').forEach((element) => {
    element.textContent = element.dataset[language];
  });

  document.querySelectorAll('[data-zh-label][data-en-label]').forEach((element) => {
    element.setAttribute('aria-label', element.dataset[`${language}Label`]);
  });

  languageCurrent.textContent = content.current;
  languageOther.textContent = content.other;
  languageToggle.setAttribute('aria-label', content.toggleLabel);
  copyLabel.textContent = content.copy;
  localStorage.setItem('archive-apply-language', language);
  applyLineage(activeLineage, language);
}

languageToggle.addEventListener('click', () => {
  const nextLanguage = document.documentElement.dataset.lang === 'zh' ? 'en' : 'zh';
  applyLanguage(nextLanguage);
});

document.querySelectorAll('[data-lineage]').forEach((button) => {
  button.addEventListener('click', () => {
    activeLineage = button.dataset.lineage;
    document.querySelectorAll('[data-lineage]').forEach((candidate) => {
      const selected = candidate === button;
      candidate.classList.toggle('is-active', selected);
      candidate.setAttribute('aria-selected', String(selected));
    });
    applyLineage(activeLineage, document.documentElement.dataset.lang);
  });
});

document.querySelector('[data-copy-command]').addEventListener('click', async () => {
  const language = document.documentElement.dataset.lang;
  const label = languageContent[language];
  try {
    await navigator.clipboard.writeText('$archive-and-apply');
    copyLabel.textContent = label.copied;
    window.setTimeout(() => {
      copyLabel.textContent = label.copy;
    }, 1600);
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(document.querySelector('[data-command]'));
    selection.removeAllRanges();
    selection.addRange(range);
  }
});

const header = document.querySelector('[data-header]');
function updateHeader() {
  header.classList.toggle('is-scrolled', window.scrollY > 24);
}
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

const sections = [...document.querySelectorAll('main section[id]')];
const navLinks = [...document.querySelectorAll('.site-nav a')];
const sectionObserver = new IntersectionObserver((entries) => {
  const active = entries
    .filter((entry) => entry.isIntersecting)
    .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (!active) return;
  navLinks.forEach((link) => {
    link.classList.toggle('is-active', link.hash === `#${active.target.id}`);
  });
}, { rootMargin: '-20% 0px -65% 0px', threshold: [0, 0.2, 0.5] });
sections.forEach((section) => sectionObserver.observe(section));

const revealTargets = document.querySelectorAll('.section-heading, .workflow-card, .reader-stack li, .tool-grid article, .start-copy, .command-card');
revealTargets.forEach((target) => target.dataset.reveal = '');
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  revealTargets.forEach((target) => revealObserver.observe(target));
} else {
  revealTargets.forEach((target) => target.classList.add('is-visible'));
}

document.querySelector('[data-year]').textContent = new Date().getFullYear();
applyLanguage(document.documentElement.dataset.lang === 'en' ? 'en' : 'zh');

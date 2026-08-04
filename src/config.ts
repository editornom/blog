/**
 * 언어별 브랜드. Layout / Header 가 현재 경로의 언어에 맞춰 골라 씁니다.
 * SITE.title / SITE.desc 는 언어를 알 수 없는 위치(루트 등)의 기본값입니다.
 */
export const SITE_I18N = {
  ko: {
    title: "Be Dev.Log (비개발노트)",
    brand: "Be Dev.Log",
    desc: "코드 한 줄 모르는 비개발자의 실전 삽질 기록.",
  },
  en: {
    title: "Be Dev.Log",
    brand: "Be Dev.Log",
    desc: "A non-dev who knows zero code—logging real-world trial, error, and build.",
  },
  jp: {
    title: "非デブログ (Be Dev.Log)",
    brand: "Be Dev.Log",
    desc: "コード0行からの挑戦。非開発者のリアルな泥臭い奮闘記。",
  },
  cn: {
    title: "非开发手记 (Be Dev.Log)",
    brand: "Be Dev.Log",
    desc: "一行代码也不会。非开发者的真实折腾与踩坑日志。",
  },
} as const;

export type SiteLang = keyof typeof SITE_I18N;

export function siteMeta(lang?: string | null) {
  return SITE_I18N[(lang as SiteLang) ?? "ko"] ?? SITE_I18N.ko;
}

export const SITE = {
  website: "https://editornom.com/", // replace this with your deployed domain
  author: "Be Dev.Log",
  profile: "https://editornom.com/about",
  desc: SITE_I18N.ko.desc,
  title: SITE_I18N.ko.title,
  ogImage: "astropaper-og.jpg",
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 5,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
  showArchives: false,
  showBackButton: true, // show back button in post detail
  editPost: {
    enabled: true,
    text: "Edit page",
    url: "https://github.com/editornom/blog/edit/main/",
  },
  dynamicOgImage: true,
  dir: "ltr", // "rtl" | "auto"
  lang: "ko", // html lang code. Set this empty and default will be "en"
  timezone: "Asia/Seoul", // Default global timezone (IANA format) https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
} as const;
export const LOGO_IMAGE = {
  enable: true,
  svg: false,
  width: 200, // 로고 크기에 따라 이 숫자를 조절하세요
  height: 23,
};
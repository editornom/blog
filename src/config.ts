export const SITE = {
  website: "https://editornom.com/", // replace this with your deployed domain
  author: "편집",
  profile: "https://satnaing.dev/",
  desc: "IT 테크 기술 블로그 | AI, 사이버보안, 앱개발",
  title: "editorNOM's IT Blog",
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
// Place any global data in this file.
// You can import this data from anywhere in your site by using the `import` keyword.

interface SocialLink {
  href: string;
  label: string;
}

interface Site {
  website: string;
  author: string;
  profile: string;
  desc: string;
  title: string;
  ogImage: string;
  lightAndDarkMode: boolean;
  postPerIndex: number;
  postPerPage: number;
  scheduledPostMargin: number;
  showArchives: boolean;
  showBackButton: boolean;
  editPost: {
    enabled: boolean;
    text: string;
    url: string;
  };
  dynamicOgImage: boolean;
  lang: string;
  timezone: string;
}

// Site configuration
export const SITE: Site = {
  website: "https://xuanloi.me/",
  author: "Đào Xuân Lợi",
  profile: "https://xuanloi.me/about",
  desc: "Đào Xuân Lợi chia sẻ về cuộc sống, marketing và những điều tôi học được trên hành trình của mình.",
  title: "Đào Xuân Lợi",
  ogImage: "",
  lightAndDarkMode: true,
  postPerIndex: 10,
  postPerPage: 10,
  scheduledPostMargin: 15 * 60 * 1000,
  showArchives: false,
  showBackButton: false,
  editPost: {
    enabled: false,
    text: "Sửa trên GitHub",
    url: "https://github.com/Edeys/xuanloi.me/edit/main/",
  },
  dynamicOgImage: true,
  lang: "vi",
  timezone: "Asia/Ho_Chi_Minh",
};

export const SITE_TITLE = SITE.title;
export const SITE_DESCRIPTION = SITE.desc;

// Navigation links
export const NAV_LINKS: SocialLink[] = [
  {
    href: "/",
    label: "Bài viết",
  },
  {
    href: "/about",
    label: "Về tôi",
  },
];

// Social media links
export const SOCIAL_LINKS: SocialLink[] = [
  {
    href: "https://www.youtube.com/@xuanloi_mkt",
    label: "YouTube",
  },
  {
    href: "https://www.facebook.com/xuanloi.me",
    label: "Facebook cá nhân",
  },
  {
    href: "https://zalo.me/0348579065",
    label: "Zalo",
  },
  {
    href: "https://github.com/Edeys",
    label: "GitHub",
  },
  {
    href: "mailto:xuanloi.me@gmail.com",
    label: "Email",
  },
  {
    href: "/rss.xml",
    label: "RSS",
  },
];

// Category map: slug → display name
export const CATEGORY_MAP: Record<string, string> = {
  "phat-trien-ban-than": "Phát triển bản thân",
  marketing: "Marketing",
  "tam-ly-tinh-yeu": "Tâm lý & Tình yêu",
  "thuong-hieu-ca-nhan": "Thương hiệu cá nhân",
  "su-nghiep": "Sự nghiệp",
  "cuoc-song": "Cuộc sống",
  "nong-nghiep": "Nông nghiệp / Cà Phê",
};

// Icon map for social media
export const ICON_MAP: Record<string, string> = {
  YouTube: "youtube",
  Facebook: "facebook",
  "Facebook cá nhân": "facebook",
  "Số điện thoại": "phone",
  GitHub: "github",
  Email: "mail",
  RSS: "rss",
};

import { SITE } from "./consts.ts";

export const SOCIALS = [
  {
    name: "Github",
    href: "https://github.com/Edeys",
    linkTitle: ` ${SITE.title} trên Github`,
    icon: "github",
    active: true,
  },
  {
    name: "YouTube",
    href: "https://www.youtube.com/@xuanloi_mkt",
    linkTitle: ` ${SITE.title} trên YouTube`,
    icon: "youtube",
    active: true,
  },
  {
    name: "Facebook",
    href: "https://www.facebook.com/xuanloi.me",
    linkTitle: `Facebook cá nhân của ${SITE.title}`,
    icon: "facebook",
    active: true,
  },
  {
    name: "Mail",
    href: "mailto:xuanloi.me@gmail.com",
    linkTitle: `Gửi email cho ${SITE.title}`,
    icon: "mail",
    active: true,
  },
  {
    name: "Zalo",
    href: "https://zalo.me/0348579065",
    linkTitle: `Nhắn tin Zalo cho ${SITE.title}`,
    icon: "phone",
    active: true,
  },
] as const;

export const SHARE_LINKS = [
  {
    name: "Facebook",
    href: "https://www.facebook.com/sharer.php?u=",
    linkTitle: `Chia sẻ bài viết trên Facebook`,
    icon: "facebook",
  },
  {
    name: "Twitter",
    href: "https://twitter.com/intent/tweet?url=",
    linkTitle: `Chia sẻ bài viết trên Twitter/X`,
    icon: "twitter",
  },
  {
    name: "LinkedIn",
    href: "https://www.linkedin.com/sharing/share-offsite/?url=",
    linkTitle: `Chia sẻ bài viết trên LinkedIn`,
    icon: "linkedin",
  },
  {
    name: "Telegram",
    href: "https://t.me/share/url?url=",
    linkTitle: `Chia sẻ bài viết qua Telegram`,
    icon: "telegram",
  },
  {
    name: "Mail",
    href: "mailto:?subject=Xem%20bài%20viết%20này&body=",
    linkTitle: `Chia sẻ bài viết qua email`,
    icon: "mail",
  },
] as const;

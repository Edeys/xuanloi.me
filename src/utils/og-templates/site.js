import satori from "satori";
import { SITE } from "@/config";
import loadGoogleFonts from "../loadGoogleFont";

export default async () => {
  return satori(
    {
      type: "div",
      props: {
        style: {
          background: "#1a1b26",
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        },
        children: [
          {
            type: "div",
            props: {
              style: {
                position: "absolute",
                top: "-1px",
                right: "-1px",
                border: "3px solid #565f89",
                background: "#24283b",
                opacity: "0.8",
                borderRadius: "12px",
                display: "flex",
                justifyContent: "center",
                margin: "2.5rem",
                width: "88%",
                height: "80%",
              },
            },
          },
          {
            type: "div",
            props: {
              style: {
                border: "3px solid #c0caf5",
                background: "#1a1b26",
                borderRadius: "12px",
                display: "flex",
                justifyContent: "center",
                margin: "2rem",
                width: "88%",
                height: "80%",
              },
              children: {
                type: "div",
                props: {
                  style: {
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    margin: "24px",
                    width: "90%",
                    height: "90%",
                  },
                  children: [
                    {
                      type: "div",
                      props: {
                        style: {
                          display: "flex",
                          flexDirection: "column",
                          justifyContent: "center",
                          alignItems: "center",
                          height: "85%",
                          maxHeight: "85%",
                          overflow: "hidden",
                          textAlign: "center",
                        },
                        children: [
                          {
                            type: "p",
                            props: {
                              style: {
                                fontSize: 56,
                                fontWeight: "bold",
                                color: "#c0caf5",
                                lineHeight: 1.3,
                                margin: "0 16px",
                              },
                              children: SITE.title,
                            },
                          },
                          {
                            type: "p",
                            props: {
                              style: {
                                fontSize: 22,
                                color: "#9aa5ce",
                                marginTop: "12px",
                              },
                              children: SITE.desc,
                            },
                          },
                        ],
                      },
                    },
                    {
                      type: "div",
                      props: {
                        style: {
                          display: "flex",
                          justifyContent: "space-between",
                          width: "100%",
                          fontSize: 20,
                          borderTop: "1px solid #565f89",
                          paddingTop: "12px",
                        },
                        children: [
                          {
                            type: "span",
                            props: {
                              style: { color: "#9aa5ce" },
                              children: "by Đào Xuân Lợi",
                            },
                          },
                          {
                            type: "span",
                            props: {
                              style: { color: "#7aa2f7", fontWeight: "bold" },
                              children: "xuanloi.me",
                            },
                          },
                        ],
                      },
                    },
                  ],
                },
              },
            },
          },
        ],
      },
    },
    {
      width: 1200,
      height: 630,
      embedFont: true,
      fonts: await loadGoogleFonts(SITE.title + SITE.desc + "xuanloi.me" + "by"),
    },
  );
};

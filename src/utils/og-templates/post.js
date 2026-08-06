import satori from "satori";
import loadGoogleFonts from "../loadGoogleFont";

export default async (post) => {
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
                          alignItems: "flex-start",
                          height: "85%",
                          maxHeight: "85%",
                          overflow: "hidden",
                        },
                        children: [
                          {
                            type: "p",
                            props: {
                              style: {
                                fontSize: 72,
                                fontWeight: "bold",
                                color: "#c0caf5",
                                lineHeight: 1.2,
                              },
                              children: post.data.title,
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
                          fontSize: 22,
                          borderTop: "1px solid #565f89",
                          paddingTop: "12px",
                        },
                        children: [
                          {
                            type: "span",
                            props: {
                              style: { color: "#9aa5ce" },
                              children: `by ${post.data.author}`,
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
      fonts: await loadGoogleFonts(post.data.title + post.data.author + "xuanloi.me"),
    },
  );
};

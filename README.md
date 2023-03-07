# astro-theme-scraper

Scrape all of the pages at https://astro.build/themes/1, https://astro.build/themes/2, until https://astro.build/themes/*. Here's the data needed.

On https://astro.build/themes/1

```js
# array of theme objects
[
  {
    name: "AstroPaper",
    description: "A minimal, accessible and SEO-friendly Astro blog theme.",
    link: "https://astro.build/themes/details/astro-paper",
    image: "https://astro.build/_astro/astro-paper-hero.dc566b94.webp"
  },
  ...
]
```

Then, for each theme in the array you make, visit the link and get the following. 

On https://astro.build/themes/details/astro-paper/

```js
{
  getStartedLink: "https://github.com/satnaing/astro-paper",
  liveDemoLink: "https://astro-paper.pages.dev/"
}
```

Finally, merge the two data sets so that we have one big array with the following:

```js
[
  {
    name: "AstroPaper",
    description: "A minimal, accessible and SEO-friendly Astro blog theme.",
    link: "https://astro.build/themes/details/astro-paper",
    image: "https://astro.build/_astro/astro-paper-hero.dc566b94.webp",
    getStartedLink: "https://github.com/satnaing/astro-paper",
    liveDemoLink: "https://astro-paper.pages.dev/"
  },
  ...
]
```

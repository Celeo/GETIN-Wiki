import marked from 'marked'


export const renderer = new marked.Renderer()
renderer.heading = (text, level) => {
  return `<h${level} class="title is-${level}">${text}</h${level}>`
}

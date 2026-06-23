import { onMounted, onUnmounted } from 'vue'

export function useScrollReveal() {
  let observer = null
  let mutationObserver = null

  onMounted(() => {
    // Create the IntersectionObserver
    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed')
          observer.unobserve(entry.target)
        }
      })
    }, {
      threshold: 0, // Trigger as soon as 1 pixel is visible
      rootMargin: '0px 0px -50px 0px'
    })

    // Function to find and observe all data-reveal elements
    const observeElements = () => {
      const elements = document.querySelectorAll('[data-reveal]:not(.revealed):not([data-observing])')
      elements.forEach(el => {
        el.setAttribute('data-observing', 'true')
        observer.observe(el)

        // Failsafe: if the element is already extremely high up on the page, force reveal
        const rect = el.getBoundingClientRect()
        if (rect.top < window.innerHeight) {
          setTimeout(() => el.classList.add('revealed'), 100) // slight delay for smooth initial load
        }
      })
    }

    // Run observing logic slightly after mount to guarantee DOM is ready
    setTimeout(observeElements, 50)

    // Watch for dynamically added elements (like modals rendering in the DOM)
    mutationObserver = new MutationObserver(() => {
      observeElements()
    })

    mutationObserver.observe(document.body, {
      childList: true,
      subtree: true
    })
  })

  onUnmounted(() => {
    if (observer) observer.disconnect()
    if (mutationObserver) mutationObserver.disconnect()
  })
}

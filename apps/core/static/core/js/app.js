gsap.registerPlugin(ScrollTrigger, ScrollSmoother)

// срабатывает только не на телефонах 
if (ScrollTrigger.isTouch !==1){
    // плавный скролл
    ScrollSmoother.create({
        wrapper: '.wrapper',
        content: '.content',
        smooth: 1.5,
        effects: true,
    })

    // прозрачность верхней части при прокрутке
    gsap.fromTo('.hero-section', { opacity: 1 }, {
        opacity: 0, 
        scrollTrigger:{
            trigger: '.hero-section',
            start: 'center',
            end: '850',
            scrub: true
        }
    })

    // цикл для появления каждого элемента сбоку (левая сторона)
    let itemsL = gsap.utils.toArray('.gallery__left .gallery__item')

    itemsL.forEach(item => {
        gsap.fromTo(item, {x: -800, opacity:0}, {
            opacity: 1, x:0,
            scrollTrigger: {
                trigger: item,
                start: '-2000',
                end: '-100',
                scrub: true
            }
        })
    })

    let itemsR = gsap.utils.toArray('.gallery__right .gallery__item')

    itemsR.forEach(item => {
        gsap.fromTo(item, {x: 800, opacity:0}, {
            opacity: 1, x:0,
            scrollTrigger: {
                trigger: item,
                start: '-2000',
                end: '200',
                scrub: true
            }
        })
    })
}
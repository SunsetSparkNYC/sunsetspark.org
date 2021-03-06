---
layout: default
title: About
permalink: /about/
excerpt: Everything you ever wanted to know about the people that run Sunset Spark.
---

<section>
    <h2 class="section-heading">History</h2>
    <p>Sunset Spark unofficially started in the Summer of 2008 when Yadira and Gaelen taught 3rd and 4th graders soldering and robotics at P.S. 24 in Brooklyn. In 2013, they began pursuing Sunset Spark's mission full-time by partnering with neighborhood schools to provide in-class creative technology instruction. With a bootstrapped budget and two people, an educator & an engineer, we teach over 3,000 kids creative technology skills yearly.</p>
</section>

<hr class="heart">

<section>
  <h2 class="section-heading">Yadira &amp; Gaelen Hadlett</h2>
  <div class="grid wrap">
    <div class="unit half align-right center-on-mobiles">
      <img id="about-family-image" src="/img/about_family_frame.png" alt="Gaelen and Yadira Hadlett" />
    </div>
    <div class="unit half">
      <p>
      <span class="lead">Yadira</span> has a B.A. in International Studies from Seattle University and an M.Ed. in Social & Comparative Analysis in Education from the University of Pittsburgh.  She served in Peace Corp as a primary and secondary English teacher in Bulgaria.  After graduate school, she ran a large, highly regarded K-5 bilingual after school program focusing on social emotional learning.  She co-founded Sunset Spark to bring more fun and creative science classes to immigrant families. She enjoys bringing culture and tech together for more relevant and exciting classes for families.
      </p><p>
      <span class="lead">Gaelen</span> holds a B.S. and M.S. in computer science from the University of Central Florida.  In his 10 years as a professional software engineer, he built useful things like medical language learning software, playful things like mobile games, and destructive things like weapon training systems.  Looking for more out of coding, he started teaching experimental tech classes to K-8 students early on in his coding career. After co-founding Sunset Spark, he studied Neuroscience and Education at Teachers College, Columbia University to bring more science-backed learning experiences to the community.
      </p>
    </div>
  </div>
</section>

<hr class="heart">

{% include donate.html %}

<script>
  window.addEventListener('load', function() {
      let animatedUrl = '/img/about_family.gif';
      let image = new Image()
      image.addEventListener('load', () => document.getElementById('about-family-image').src = animatedUrl)
      image.src = animatedUrl
  })
</script>

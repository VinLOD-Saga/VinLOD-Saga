<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  
  <xsl:template match="tei:TEI">
    <html lang="en">
      <head>
          <meta charset="UTF-8"/>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
          <title>The Finding of Wineland the Good</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
      </head>
      <!-- Header -->
      <body class="d-flex flex-column align-items-center">
        <div class="container m-3 p-3" id="heading">
          <h2>The Finding of Wineland the Good - Excerpted Digital Edition</h2>
          <h4><xsl:value-of select="tei:text//tei:body/tei:note"/></h4>
        </div>
        
        <!-- Main Text -->
        <div class="container m-3 p-3" id="body">
          <section n="1">
            <p>Lorem ipsum dolor sit amet <a data-bs-toggle="offcanvas" href="#offcanvasExample" role="button" aria-controls="offcanvasExample" data-target-id="3">consectetur</a> adipisicing elit. Ut asperiores voluptas repellat nostrum maxime et blanditiis doloribus sint, debitis obcaecati alias? Cumque laboriosam voluptatum corporis quis ea adipisci modi quia explicabo praesentium doloribus excepturi culpa officia aperiam soluta enim deserunt consectetur sed itaque, voluptates eos sequi commodi sapiente magni! Optio!</p>
          </section>
          <section n="2">
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quidem, laudantium nostrum maiores soluta suscipit exercitationem maxime odit, ex voluptates velit animi laboriosam, non optio. Ducimus iusto debitis, quod, atque tenetur quisquam facere numquam sit repellendus libero laborum corporis vel in cupiditate magnam quaerat temporibus. Explicabo rerum pariatur saepe cumque laboriosam?</p>
          </section>
          <section n="3">
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Vel dolores quaerat dicta sunt asperiores. Deserunt qui temporibus est numquam voluptatem omnis suscipit neque labore voluptas error culpa quibusdam, minus animi quas incidunt illum quasi excepturi possimus harum, porro, ullam deleniti hic. Aut, iure <a data-bs-toggle="offcanvas" href="#offcanvasExample" role="button" aria-controls="offcanvasExample" data-target-id="4">aliquid</a> nobis architecto quidem ipsam voluptatum quia?</p>
          </section>
          <section n="4">
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Eaque voluptates tenetur fugiat consequuntur dolores nulla cum dicta consectetur, in repellendus recusandae odit sapiente molestiae <a href="#" data-bs-toggle="popover" data-bs-title="Popover title" data-bs-content="And here’s some amazing content. It’s very engaging. Right?">doloribus</a> quas, quam eos qui maiores, aliquid obcaecati? Rerum voluptas dicta delectus. Iste ad assumenda incidunt delectus quo, asperiores, quibusdam vero quos voluptas sit, odit exercitationem.</p>
          </section>
          <section n="5">
            <p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Animi odit, beatae labore repellat optio hic qui neque quidem cumque repellendus eos non nulla dolorum quam deleniti natus cupiditate. Doloribus nam ipsum magnam iure autem a dolorum exercitationem esse at modi ad, veniam vero illo dicta quos veritatis eligendi! Rem, itaque.</p>
          </section>
          <section n="6">
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Iure quibusdam veritatis deserunt explicabo! Molestiae explicabo modi autem, ex quisquam ducimus, temporibus ratione aliquam corporis eveniet nesciunt, quas sapiente. Magnam amet sed id neque perferendis, sunt blanditiis ullam molestias, error aut fugiat debitis, quasi nesciunt culpa quam. Dicta natus quis quasi.</p>
          </section>
          <section n="7">
            <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptate eveniet dignissimos adipisci, dolorem fugiat vero provident. Alias mollitia eligendi assumenda asperiores, ex sequi aspernatur architecto eos cumque eaque ipsum dolor nam, ullam, dolorum ea molestiae animi libero repellendus? Totam explicabo reprehenderit atque sit possimus nostrum veniam delectus quis quod quibusdam.</p>
          </section>
          <section n="8">
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus, dolorum perferendis iste, optio nesciunt a distinctio odio asperiores rem vel expedita, beatae enim similique? Quod, unde? Est non vero <a data-bs-toggle="offcanvas" href="#offcanvasExample" role="button" aria-controls="offcanvasExample" data-target-id="5">magni</a> esse quo aperiam porro nihil, placeat possimus error facere aspernatur reprehenderit quae perspiciatis quasi ducimus amet rerum exercitationem! In, ad?</p>
          </section>
        </div>
        
        <!-- Off Canvas Text -->
        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
          <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasExampleLabel">End Notes</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <section id="3" style="margin-bottom: 300px;">
              <h6>Note 3</h6>
              <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias harum, porro iusto facilis laboriosam temporibus libero vero deleniti doloremque molestias, quia similique quod deserunt ab, aperiam consequatur reiciendis velit provident ratione amet excepturi commodi praesentium. Odit suscipit repellat fuga. Laudantium, perferendis eaque assumenda modi doloribus officia alias enim quos accusamus.</p>
            </section>
            <section id="4" style="margin-bottom: 300px;">
              <h6>Note 4</h6>
              <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias harum, porro iusto facilis laboriosam temporibus libero vero deleniti doloremque molestias, quia similique quod deserunt ab, aperiam consequatur reiciendis velit provident ratione amet excepturi commodi praesentium. Odit suscipit repellat fuga. Laudantium, perferendis eaque assumenda modi doloribus officia alias enim quos accusamus.</p>
            </section>
            <section id="5" style="margin-bottom: 300px;">
              <h6>Note 5</h6>
              <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias harum, porro iusto facilis laboriosam temporibus libero vero deleniti doloremque molestias, quia similique quod deserunt ab, aperiam consequatur reiciendis velit provident ratione amet excepturi commodi praesentium. Odit suscipit repellat fuga. Laudantium, perferendis eaque assumenda modi doloribus officia alias enim quos accusamus.</p>
            </section>
          </div>
        </div>

        <!-- bootstrap script -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <!-- popover script -->
        <script>
          const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
          const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
        </script>
        <!-- Scrolling in offcanvas script -->
        <script>
          // Attach listener to all offcanvas trigger links
          document.querySelectorAll('[data-bs-toggle="offcanvas"]').forEach(link => {
            link.addEventListener('click', function () {
              const targetId = this.getAttribute('data-target-id');
              const offcanvas = document.getElementById('offcanvasExample');
              const bsOffcanvas = bootstrap.Offcanvas.getOrCreateInstance(offcanvas);
          
              offcanvas.addEventListener('shown.bs.offcanvas', function handler() {
                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                  targetEl.scrollIntoView({ behavior: 'smooth' });
              
                // Optional highlight
                // targetEl.classList.add('bg-warning', 'p-2');
                // setTimeout(() => {
                //     targetEl.classList.remove('bg-warning', 'p-2');
                // }, 1500);
                }
              
                // Remove the listener after one execution
                offcanvas.removeEventListener('shown.bs.offcanvas', handler);
              });
            });
          });
        </script>
      </body>
    </html>
  </xsl:template>
    

</xsl:stylesheet>
  


                
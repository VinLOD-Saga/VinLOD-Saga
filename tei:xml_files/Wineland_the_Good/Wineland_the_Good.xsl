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
        <xsl:apply-templates select="tei:text//tei:body/tei:div[@type='translation']"/>

        <!-- Off Canvas Notes -->
        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNotes" aria-labelledby="offcanvasNotesLabel">
          <div class="offcanvas-header">
            <h5 class="offcanvas-title mx-auto text-uppercase" id="offcanvasNotesLabel"><xsl:value-of select="tei:text//tei:back//tei:head"/></h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <xsl:apply-templates select="tei:text//tei:back//tei:noteGrp"/>
          </div>
        </div>
        
        <!-- bootstrap script -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <!-- popover script -->
        <script>
          const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
          const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl, {
            container: 'body',
            trigger: 'hover focus',  // or your preferred triggers
            delay: { "show": 0, "hide": 200 } // optional delay to smooth appearance
            });
          });
        </script>
        <!-- Scrolling in offcanvas script -->
        <script>
          // Attach listener to all offcanvas trigger links
          document.querySelectorAll('[data-bs-toggle="offcanvas"]').forEach(link => {
            link.addEventListener('click', function () {
              const targetId = this.getAttribute('data-target-id');
              const offcanvas = document.getElementById('offcanvasNotes');
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
  <!-- Template for main text -->
  <xsl:template match="tei:div[@type='translation']">
    <div class="container m-3 p-3" id="body"><xsl:apply-templates/></div>
  </xsl:template>
  
  <!-- Template for title -->
  <xsl:template match="tei:head[@rend='align(center) case(allcaps)']">
    <h4 class="text-uppercase text-center"><xsl:value-of select="."/></h4>
  </xsl:template>
  
  <!-- Template for paragraph -->
  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>
  
  <!-- Template for story sections -->
  <xsl:template match="tei:seg">
    <section><xsl:apply-templates/></section>
  </xsl:template>

  <!-- Identity template to copy text and elements by default -->
  
  <xsl:template match="@*|node()">
    <!-- @*|node() - select all attributes and all child nodes of the current node  -->
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- Template for people mentioned -->

  <!-- Create a key for quick person lookup by xml:id -->
  <xsl:key name="personID" match="tei:person" use="@xml:id" />
  <!-- Template to handle persName with ref attribute -->
  <xsl:template match="tei:persName[@ref]">
    <!-- seperate the # from the reference id and save it in a variable  -->
    <xsl:variable name="persId" select="substring-after(@ref, '#')" />
    <!-- call the key with name personID which will match a person element with the $id variable -->
    <!-- save the found node in another variable -->
    <xsl:variable name="person" select="key('personID', $persId)" />
    <xsl:choose>
      <xsl:when test="$person and $person/@sameAs">
        <!-- Output persName text as a link to sameAs URI -->
        <a href="{$person/@sameAs}" target="_blank">
          <xsl:apply-templates select="node()"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <!-- Create a popover with information about the person -->
        <xsl:variable name="persName" select="$person/tei:persName"/>
        <xsl:variable name="persNote" select="$person/tei:note"/>
        <a href="#" data-bs-toggle="popover" data-bs-title="{string($persName)}" data-bs-content="{string($persNote)}"><xsl:apply-templates select="node()"/></a>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <!-- Template for places mentioned -->

  <!-- Create a key for quick place lookup by xml:id -->
  <xsl:key name="placeID" match="tei:place" use="@xml:id" />
  <xsl:template match="tei:placeName[@ref]">
    <!-- seperate the # from the reference id and save it in a variable  -->
    <xsl:variable name="plId" select="substring-after(@ref, '#')" />
    <!-- call the key with name placeID which will match a place element with the $plId variable -->
    <!-- save the found node in another variable -->
    <xsl:variable name="place" select="key('placeID', $plId)" />
    <xsl:choose>
      <xsl:when test="$place/@sameAs">
        <!-- Output placeName text as a link to sameAs URI -->
        <a href="{ $place/@sameAs }" target="_blank">
          <xsl:apply-templates select="node()"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <!-- Create a popover with information about the place -->
        <xsl:variable name="placeName" select="$place/tei:placeName"/>
        <xsl:variable name="placeNote" select="$place/tei:note"/>
        <a href="#" data-bs-toggle="popover" data-bs-title="{string($placeName)}" data-bs-content="{string($placeNote)}"><xsl:apply-templates select="node()"/></a>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <!-- Template for footnotes -->
  <xsl:template match="tei:note[@place='bottom']">
    <xsl:variable name="noteText" select="normalize-space(.)"/>
    <a href="#" data-bs-toggle="popover" data-bs-title="Note" data-bs-content="{string($noteText)}">
      <xsl:text>*</xsl:text>
    </a>
  </xsl:template>
  
  <!-- Template for variant readings -->

  <!-- Key to apparatus -->
  <xsl:key name="appKey" match="tei:app" use="@loc" />
  <!-- Key to witnesses -->
  <xsl:key name="witKey" match="tei:witness" use="@xml:id" />
  
  <xsl:template match="tei:span[@n]">
    <xsl:variable name="app" select="key('appKey',@n)"/>
    <xsl:variable name="reading" select="$app/tei:rdg"/>
    <xsl:variable name="witID" select="substring-after($reading/@wit, '#')"/>
    <xsl:variable name="witness" select="key('witKey', $witID)"/>
    <a href="#" data-bs-toggle="popover" data-bs-title="{string($witness)}" data-bs-content="{string($reading)}"><xsl:apply-templates select="node()" /></a>
  </xsl:template>
  
  <!-- Template for endnotes (back) -->  
  <xsl:template match="tei:note[@xml:id]">
    <section id="{@xml:id}">
      <h6><xsl:value-of select="@xml:id"/></h6>
      <xsl:apply-templates select="node()" />
    </section>
  </xsl:template>
  
  <!-- Template for endnotes (main text) -->
  <xsl:template match="tei:note[@place='end']">
    <xsl:variable name="endnoteID" select="substring-after(@target, '#')"/>
    <a data-bs-toggle="offcanvas" href="#offcanvasNotes" role="button" aria-controls="offcanvasNotes" data-target-id="{string($endnoteID)}"><xsl:value-of select="."/></a>
  </xsl:template>
</xsl:stylesheet>
  


                
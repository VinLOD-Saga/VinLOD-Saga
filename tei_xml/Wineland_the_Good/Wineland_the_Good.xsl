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
        
          <!-- Fonts -->
          <link rel="preconnect" href="https://fonts.googleapis.com"/>
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
          <link href="https://fonts.googleapis.com/css2?family=Encode+Sans:wght@100..900&amp;family=Forum&amp;family=Metamorphous&amp;display=swap" rel="stylesheet"/>
        
          <!-- Main CSS File -->
          <!-- <link href="tei_xml/Wineland_the_Good/wineland.css" rel="stylesheet"/> -->
          <style>
              .metamorphous-regular {
              font-family: "Metamorphous", serif;
              font-weight: 400;
              font-style: normal;
              }
              
              .forum-regular {
              font-family: "Forum", serif;
              font-weight: 400;
              font-style: normal;
              }

              .encode-sans-light {
              font-family: "Encode Sans", sans-serif;
              font-optical-sizing: auto;
              font-weight: 300;
              font-style: normal;
              font-variation-settings:
              "wdth" 100;
              }
          
              a, span {
                color: black;
              }
          
              a:hover, span:hover {
                <!-- color: #500E0E; -->
                color: color-mix(in srgb, #500E0E, transparent 30%);
              }
          
              body {
                background-color: #E7E6E0;
                font-size: 18px;
              }
          
              .main {
                display: flex;
                flex-direction: column;
                align-items: center; 
                margin-top: 20px;
          
              }
          
              .offcanvas {
                background-color: #E7E6E0;
                font-size: 18px;
              }
          
              .header {
                --background-color: rgba(0, 0, 0, 0);
                --default-color: #ffffff;
                --heading-color: #ffffff;
                color: #1b3342;
                background-color: #E7E6E0;
                <!-- padding: 20px 0; -->
                transition: all 0.5s;
                z-index: 997;
              }
              
              .header .logo {
                line-height: 1;
              }
              
              .header .logo img {
                max-height: 60px;
                margin-right: 8px;
                margin-top: 10px;
              }
              
              .header .logo h1 {
                font-size: 20px;
                margin: 0;
                font-weight: 700;
                color: #1b3342;
              }
              
              .header .cta-btn,
              .header .cta-btn:focus {
                color: #E7E6E0;
                font-size: 13px;
                padding: 7px 25px;
                margin: 0 0 0 30px;
                border-radius: 4px;
                transition: 0.3s;
                text-transform: uppercase;
                border: 2px solid #E7E6E0;
              }
              
              .header .cta-btn:hover,
              .header .cta-btn:focus:hover {
                color: #E7E6E0;
                background: #500E0E;
                border-color: #500E0E;
              }
          
              .heading {
                margin-bottom: 20px ;
              }
          
              hr {
                height: 4px !important;            
                background-color: #1b3342; 
                color: #1b3342;
                border: none; 
                opacity: 0.80;
              }
          
              .separatorOne {
                background: linear-gradient(rgba(2, 2, 2, 0.5), rgba(0, 0, 0, 0.5)), url("/assets/img/leif_painting.jpg") fixed center center;
                background-size: cover;
                padding: 300px 0;
                min-height: 300px;
                align-self: stretch; 
                width: 100%; 
              }
          
              #editorNote {
                margin-top:35px;
              }
          
              .offcanvas-header {
                background-color : #1b3342; 
                color: #EFF3F0 ;
              }
          
              .btn-close {
                filter: brightness(0) saturate(100%) invert(93%) sepia(3%) saturate(285%) hue-rotate(75deg) brightness(106%) contrast(96%);
              }
          </style>

      </head>
      
      <!-- Body -->
      <body> 
        <!-- class="align-items-center m-3 p-3" -->
        <!-- Header -->
        <header id="header" class="header align-items-center justify-content-start">
          <div class="container-fluid container-xl position-relative d-flex align-items-center m-0">
            <a href="/index.html" class="logo d-flex align-items-center">
              <!-- Uncomment the line below if you also wish to use an image logo -->
              <img src="/assets/img/Vinlod_logo_full.png" alt=""/>
              <!-- <h1 class="sitename metamorphous-regular">VinLOD Saga</h1> -->
            </a>
          </div>
        </header>
        
        <!-- Main content -->
        <main class="main">
          
          <div class="container align-items-center justify-content-center p-3" id="heading">
            <h2 class="metamorphous-regular text-center">The Finding of Wineland the Good - Excerpted Digital Edition</h2>
            <hr/>
            <p class="forum-regular "><xsl:value-of select="tei:teiHeader//tei:projectDesc/tei:p"/></p>
          </div>
          
          <!-- === Background effect SEPARATOR === -->
          <section id="separatorOne" class="separatorOne"></section>
          <!-- End Separator -->
          
          <!-- Main Text -->
          <div class="container" id="editorNote">
            <p class="forum-regular text-center">
              <xsl:variable name="editor" select="tei:teiHeader//tei:listPerson/tei:person[@xml:id='AMR']"/>
              <xsl:variable name="annotator" select="tei:teiHeader//tei:listPerson/tei:person[@xml:id='RM']"/>
              <i>The following extracted text has be taken from two manuscript sources, <xsl:apply-templates select="tei:teiHeader//tei:listWit/tei:witness[@xml:id='EsR']"/> and <xsl:apply-templates select="tei:teiHeader//tei:listWit/tei:witness[@xml:id='THsK']"/>. The orginal text was translated and edited by <a href="{$editor/@source}" target="_blank"><xsl:value-of select="tei:teiHeader//tei:listPerson/tei:person[@xml:id='AMR']"/></a> which was then transcribed and annoted into this digital text by <a href="{$annotator/@source}" target="_blank"><xsl:value-of select="tei:teiHeader//tei:listPerson/tei:person[@xml:id='RM']"/></a>.</i>
            </p>
          </div>
          
          <xsl:apply-templates select="tei:text//tei:body/tei:div[@type='translation']"/>
        </main>

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
            trigger: 'click',  // or your preferred triggers
            <!-- delay: { "show": 0, "hide": 200 } // optional delay to smooth appearance -->
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
    <div class="container m-3 p-1" id="body"><xsl:apply-templates/></div>
  </xsl:template>
  
  <!-- Template for title -->
  <xsl:template match="tei:head[@rend='align(center) case(allcaps)']">
    <h4 class="text-uppercase text-center forum-regular" style="font-size: 25px;"><xsl:value-of select="."/></h4>
  </xsl:template>
  
  <!-- Template for paragraph -->
  <xsl:template match="tei:p">
    <p class="forum-regular"><xsl:apply-templates/></p>
  </xsl:template>
  
  <!-- Template for story sections -->
  <xsl:template match="tei:seg">
    <section><p class="forum-regular"><xsl:apply-templates/></p></section>
  </xsl:template>
  
  <!-- Template for foreign text -->
  <xsl:template match="tei:foreign">
    <i><xsl:apply-templates/></i>
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
      <xsl:when test="$person and $person/@source">
        <!-- Output persName text as a link to sameAs URI -->
        <a href="{$person/@source}" target="_blank">
          <xsl:apply-templates select="node()"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <!-- Create a popover with information about the person -->
        <xsl:variable name="persName" select="$person/tei:persName"/>
        <xsl:variable name="persNote" select="$person/tei:note"/>
        <span role="button" tabindex="0" class="popover-trigger text-decoration-underline" data-bs-toggle="popover" data-bs-title="{string($persName)}" data-bs-content="{string($persNote)}">
          <xsl:apply-templates select="node()" />
        </span>
        <!-- <a href="#" data-bs-toggle="popover" data-bs-title="{string($persName)}" data-bs-content="{string($persNote)}"><xsl:apply-templates select="node()"/></a> -->
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
      <xsl:when test="$place/@source">
        <!-- Output placeName text as a link to sameAs URI -->
        <a href="{$place/@source}" target="_blank">
          <xsl:apply-templates select="node()"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <!-- Create a popover with information about the place -->
        <xsl:variable name="placeName" select="$place/tei:placeName"/>
        <xsl:variable name="placeNote" select="$place/tei:note"/>
        <span role="button" tabindex="0" class="popover-trigger text-decoration-underline" data-bs-toggle="popover" data-bs-title="{string($placeName)}" data-bs-content="{string($placeNote)}">
          <xsl:apply-templates select="node()" />
        </span>
        <!-- <a href="#" data-bs-toggle="popover" data-bs-title="{string($placeName)}" data-bs-content="{string($placeNote)}"><xsl:apply-templates select="node()"/></a> -->
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <!-- Template for footnotes -->
  <xsl:template match="tei:note[@place='bottom']">
    <xsl:variable name="noteText" select="normalize-space(.)"/>
    <span role="button" tabindex="0" class="popover-trigger" data-bs-toggle="popover" data-bs-title="Note" data-bs-content="{string($noteText)}" style="font-size: 25px; font-weight: bold;">
      <xsl:text>*</xsl:text>
    </span>
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
    <!-- <a href="#" data-bs-toggle="popover" data-bs-title="{string($witness)}" data-bs-content="{string($reading)}"><xsl:apply-templates select="node()" /></a> -->
    <span role="button" tabindex="0" class="popover-trigger text-decoration-underline" data-bs-toggle="popover" data-bs-title="{string($witness)}" data-bs-content="{string($reading)}">
      <xsl:apply-templates select="node()" />
    </span>
    <!-- style="color: #2C6555; cursor: pointer;" -->
  </xsl:template>
  
  <!-- Template for endnotes (back) -->  
  <xsl:template match="tei:note[@xml:id]">
    <section id="{@xml:id}">
      <xsl:variable name="noteID" select="@xml:id"/>
      <xsl:variable name="noteNumber" select="substring-after($noteID, '-')"/>
      <h6 class="text-center" style="color: #500E0E">Note <xsl:value-of select="$noteNumber"/></h6>
      <xsl:apply-templates select="node()" />
    </section>
  </xsl:template>
  
  <!-- Template for endnotes (main text) -->
  <xsl:template match="tei:note[@place='end']">
    <xsl:variable name="endnoteID" select="substring-after(@target, '#')"/>
    <a data-bs-toggle="offcanvas" href="#offcanvasNotes" role="button" aria-controls="offcanvasNotes" data-target-id="{string($endnoteID)}"><xsl:value-of select="."/></a>
  </xsl:template>
  
  <!-- Template for Witness manuscripts -->
  <xsl:template  match="tei:witness">
    <xsl:variable name="witURI" select="@source"/>
    <a href="{$witURI}" target="_blank"><xsl:value-of select="."/></a>
  </xsl:template>
  
  <!-- Template for contributors -->
  <xsl:template  match="tei:listPerson[@type='contributor']/tei:person">
    <xsl:variable name="contributorURI" select="person[@source]"/>
    <a href="{$contributorURI}" target="_blank"><xsl:value-of select="tei:person/tei:persName"/></a>
  </xsl:template>
</xsl:stylesheet>

  


                
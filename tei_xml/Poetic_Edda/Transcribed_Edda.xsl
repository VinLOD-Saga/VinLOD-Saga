<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">
    
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    
    <!-- Main template matching the root -->
    <xsl:template match="tei:TEI">
        <html>
            <head>
                <!-- Fonts -->
                <link rel="preconnect" href="https://fonts.googleapis.com"/>
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
                <link href="https://fonts.googleapis.com/css2?family=Encode+Sans:wght@100..900&amp;family=Forum&amp;family=Metamorphous&amp;display=swap" rel="stylesheet"/>
                <link rel="icon" href="assets/img/Vinlod_logo_small.png" type="image/png"/>
                <title>Grimnismol- The Poetic Edda</title>
                <style>
                    .back-to-top {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    padding: 0.6em 1em;
                    font-size: 1.5em;
                    background-color: #641818;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                    opacity: 0.7;
                    transition: opacity 0.3s;
                    font-size: 2em;
                    }
                    
                    .back-to-top:hover {
                    opacity: 1;
                    }
                    body {
                    font-family: "Forum", serif;
                    font-size: 1.3em;
                    line-height: 1.6;
                    margin: 1em 5em 5em 5em;
                    padding: 0.5em 1em;
                    background-color: #0C222F;
                    color: #E7E6E0;
                    }
                    body h1 {
                    font-size: 3em;
                    text-align: center;
                    font-weight: bold;
                    margin: 0.1em 0 0.2em 0;
                    font-family: "Metamorphous", serif;
                    color: #E7E6E0;
                    }
                    body h2 {
                    text-align: center;
                    font-style: italic;
                    margin: 0.1em 0 0.2em 0;
                    color: #E7E6E0;
                    }
                    h4 {
                    text-align: center;
                    font-size: 0.7em;
                    margin: 0.1em 0 0.2em 0;
                    }
                    .head {
                    text-align: center;
                    font-style: italic;
                    margin: 0.1em 0 0.2em 0;
                    color: #0C222F;
                    }
                    .stanza {
                    text-align: center;
                    margin: 1em auto;
                    }
                    .line {
                    display: block;
                    }
                    .noteGrp {
                    margin: 1em;
                    padding: 1em;
                    border: 4px solid #5e0c0c;
                    }
                    .note, .commentary {
                    font-family: "Encode Sans", sans-serif;
                    font-size: 1em; 
                    }
                    a {
                    color: color-mix(in srgb,rgb(218, 15, 15), transparent 5%);
                    text-decoration: underline;
                    cursor: pointer;
                    }
                    a:visited {
                    color:color-mix(in srgb,rgb(183, 130, 195), transparent 20%);
                    }
                    a:hover, span:hover {
                    color: color-mix(in srgb,rgb(148, 23, 23), transparent 20%);
                    }
                    h1, h2 {
                    color: #0C222F;
                    }
                    .commentary, .personal {
                    margin: 1.5em auto;
                    font-size: 0.85em;
                    padding: 1.2em 1.5em;
                    line-height: 1.6;
                    max-width: 170ch;
                    border: 4px solid #5e0c0c
                    }
                    .commentary, .personal, .noteGrp{
                    background-color:rgba(231, 230, 224);
                    color:  #0C222F;
                    }
                    .personal {
                    max-height: 100px; 
                    overflow-y: auto;
                    border-left: 4px solid #ccc;
                    box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);                    }
                </style>
                <script>
                    function scrollToTop() {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                </script>
            </head>
            <body> <!-- Obtaining the main text. Everything is being handled by the templates.-->
                <xsl:apply-templates select="tei:text//tei:front"/>
                <xsl:apply-templates select="tei:text//tei:body"/>
                <xsl:apply-templates select="tei:text//tei:back"/>
                <button onclick="scrollToTop()" class="back-to-top">↟</button>
            </body>
            <footer style="background-color: rgba(191, 202, 202, 0.3); color: black; text-align: center; padding: 15px 150px;">
                <p>Project completed for the course Digital Humanities and Digital Knowledge, University of Bologna, 2025.</p>
                <p>Author: Ilaria De Dominicis</p>
                <p>© 2025 All rights reserved.</p>
            </footer>
        </html>
    </xsl:template>
    
    <!-- Template for main Grimnismol -->
    <xsl:template match="tei:head[@type='main']">
        <h1><xsl:value-of select="."/></h1>
    </xsl:template>
    
    <!-- Template for The Ballad of Grimnir -->
    <xsl:template match="tei:head[@type='sub']">
        <h2><i><xsl:value-of select="."/></i></h2>
    </xsl:template>
    
    <!-- Template for author's credits -->
    <xsl:template match="tei:head[@type='credits']">
        <div><h4><xsl:apply-templates/></h4></div>
    </xsl:template>
    
    <!-- Template for general heads -->
    <xsl:template match="tei:head">
        <div style="font-weight: bold;">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <!-- Template for 'commentary' in front -->
    <xsl:template match="tei:div[@type='commentary']">
        <div class="commentary">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- Template for text's 'intro' in the body -->
    <xsl:template match="tei:div[@type='intro']">
        <div class="intro">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- Template for my intro in the body -->
    <xsl:template match="tei:div[@type='personal']">
        <div class="personal"><xsl:apply-templates/></div>
    </xsl:template>

    <!-- Template for the paragraphs to have a proper layout -->
    <xsl:template match="tei:p">
        <p><xsl:apply-templates/></p>
    </xsl:template>
    
    
    <!-- Template for stanza (lg elements) with id -->
    <xsl:template match="tei:lg">
        <div class="stanza">
            <xsl:if test="@xml:id">
                <xsl:attribute name="id">
                    <xsl:value-of select="@xml:id"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- Template for lines (l elements) -->
    <xsl:template match="tei:l">
        <div class="line">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- Template for italic text -->
    <xsl:template match="tei:hi[@rend='italic']">
        <i>
            <xsl:apply-templates/>
        </i>
    </xsl:template>
    
    <!-- Template for the quotes -->
    <xsl:template match="tei:q">
        <xsl:text>"</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>"</xsl:text>
    </xsl:template>
    
    <!-- Template for ref with target (in testo) linking to note -->
    <xsl:template match="tei:ref[@target]">
        <a href="{concat('#', substring-after(@target, '#'))}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    <!-- Template for ref with source (in note) linking back to stanza -->
    <xsl:template match="tei:ref[@source] | tei:title[@source]">
        <a href="{concat('#', substring-after(@source, '#'))}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    <!-- Template for noteGrp with id from @target -->
    <xsl:template match="tei:noteGrp">
        <div class="noteGrp">
            <xsl:if test="@target">
                <xsl:attribute name="id">
                    <xsl:value-of select="substring-after(@target, '#')"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- Template for the content of ref in note -->
    <xsl:template match="tei:ref">
        <span class="ref">
            <xsl:value-of select="."/> 
        </span>
    </xsl:template>
    
    <!-- Template for individual note -->
    <xsl:template match="tei:note">
        <div class="note">
            <xsl:choose>
                <xsl:when test="@xml:id">
                    <xsl:attribute name="id">
                        <xsl:value-of select="@xml:id"/>
                    </xsl:attribute>
                </xsl:when>
                <xsl:when test="tei:ref[@target]">
                    <xsl:attribute name="id">
                        <xsl:value-of select="substring-after(tei:ref[@target]/@target, '#')"/>
                    </xsl:attribute>
                </xsl:when>
            </xsl:choose>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- Template for persName, orgName and placeName with ref -->
    <xsl:template match="tei:persName[@ref] | tei:orgName[@ref] | tei:placeName[@ref]">
        <xsl:variable name="refId" select="substring-after(@ref, '#')"/>
        <xsl:variable name="target" select="//tei:*[@xml:id = $refId]"/>
        <xsl:variable name="sameAs" select="$target/@sameAs"/>
        <xsl:variable name="source" select="$target/@source"/>
        <xsl:variable name="targetUrl">
            <xsl:choose>
                <xsl:when test="string-length($source) &gt; 0">
                    <xsl:value-of select="$source"/>
                </xsl:when>
                <xsl:when test="string-length($sameAs) &gt; 0">
                    <xsl:value-of select="$sameAs"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="@ref"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <a href="{$targetUrl}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>

</xsl:stylesheet>

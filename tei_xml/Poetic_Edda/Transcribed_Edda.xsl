<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">
    
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    
    <!-- Main template matching the root -->
    <xsl:template match="tei:TEI">
        <html>
            <head>
                <title>VinLOD Saga's Poetic Edda</title>
                <style> <!-- a little bit of CSS for presentation and link clicking -->
                    body {
                    font-family: "Times New Roman", serif;
                    font-size: 1.2em;
                    line-height: 1.6; 
                    margin: 1em 5em 5em 5em;
                    padding: 0.5em 1em;
                    background-color: rgba(232, 232, 232, 0.78); 
                    }
                    h1 {
                    font-size: 3em;
                    text-align: center;
                    font-weight: bold;
                    }
                    h2 {
                    text-align: center;
                    font-style: italic;
                    }
                    h4 {
                    text-align: center;
                    font-size: 0.7em;
                    }
                    .head {
                    text-align: center;
                    font-style: italic;
                    }  
                    h1, h2, h4, .head {
                    margin-top: 0.1em;
                    margin-bottom: 0.2em;
                    }
                    .stanza {
                    display: block;
                    text-align: center;
                    margin: 1em auto;
                    }
                    .line {
                    display: block;
                    }
                    .noteGrp {
                    background-color: rgb(254, 255, 255);
                    margin: 1em;
                    padding: 1em 1em;
                    border-right: 4px solid #ccc;
                    font-size: 0.7em; 
                    }
                    a {
                    color: #1a0dab;
                    text-decoration: underline;
                    cursor: pointer;
                    }
                    a:visited {
                    color: #660099; /* color after the click */
                    }
                    .commentary {
                    background-color: rgb(254, 255, 255);
                    margin: 1em;
                    padding: 1em;
                    font-size: 0.7em; 
                    border-left: 4px solid #ccc;
                    }

                </style>
            </head>
            <body> <!-- Obtaining the main text -->
                <xsl:apply-templates select="tei:text//tei:front"/>
                <xsl:apply-templates select="tei:text//tei:body"/>
                <xsl:apply-templates select="tei:text//tei:back"/>
            </body>
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
    
    <!-- Template for 'intro' in the body -->
    <xsl:template match="tei:div[@type='intro']">
        <div class="intro">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- Template for the paragraphs to have a proper layout -->
    <xsl:template match="tei:p">
        <p><xsl:apply-templates/></p>
    </xsl:template>
    
    <!-- Template for the ballad div -->
    <xsl:template match="tei:div[@type='ballad']">
        <xsl:apply-templates/>
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
    
    <!-- Template for ref with target (in testo) linking to note -->
    <xsl:template match="tei:ref[@target]">
        <a href="{concat('#', substring-after(@target, '#'))}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    <!-- Template for ref with source (in note) linking back to stanza -->
    <xsl:template match="tei:ref[@source]">
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
        <a href="{$targetUrl}" target="_blank">
            <xsl:apply-templates/>
        </a>
    </xsl:template>

</xsl:stylesheet>

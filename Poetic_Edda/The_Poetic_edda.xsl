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
                <style>
                    body {
                    font-family: "Times New Roman", serif;
                    line-height: 1.6; /* Ho leggermente aumentato per uniformità */
                    text-align: justified;
                    margin: 0; 
                    padding: 0; 
                    background-color: #f4f4f4; 
                    }
                    <!-- secondo me devo fare uno ad uno, senza body o p -->
                    h1 {
                    text-align: center;
                    font-weight: bold;
                    }
                    h2 {
                    text-align: center;
                    font-style: italic;
                    }
                    .stanza {
                    display: block;
                    text-align: center;
                    margin: 1em auto;
                    font-family: "Times New Roman", serif;
                    }
                    .line {
                    display: block;
                    text-align: inherit;
                    }
                </style>
            </head>
            <body>
                <xsl:apply-templates select="tei:text//tei:front"/>
                <xsl:apply-templates select="tei:text//tei:body"/>
                <xsl:apply-templates select="tei:text//tei:back"/>
            </body>
        </html>
    </xsl:template>
    
    <!-- Template for main title -->
    <xsl:template match="tei:head[@type='main'] | tei:head">
        <h1><xsl:value-of select="."/></h1>
    </xsl:template>
    
    <!-- Template for subtitle -->
    <xsl:template match="tei:head[@type='sub']">
        <h2><i><xsl:value-of select="."/></i></h2>
    </xsl:template>
    
    <!-- Template for paragraphs with type 'paragraph' -->
    <xsl:template match="tei:p[@type='paragraph']">
        <p><xsl:apply-templates/></p>
    </xsl:template>
    
    <!-- Template for the ballad div -->
    <xsl:template match="tei:div[@type='ballad']">
        <xsl:apply-templates/>
    </xsl:template>
    
    <!-- Template for stanza (lg elements) -->
    <xsl:template match="tei:lg">
        <div class="stanza">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- Template for lines (l elements) -->
    <xsl:template match="tei:l">
        <div class="line">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!-- template for italic text -->
    <xsl:template match="tei:hi[@rend='italic']">
        <i>
            <xsl:apply-templates/>
        </i>
    </xsl:template>
    
    <!-- Template for target (in the notes) -->
    <xsl:template match="tei:ref[@target]">
        <a href="{@target}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    
    <!-- templates for persName and placeName could go here -->
</xsl:stylesheet>


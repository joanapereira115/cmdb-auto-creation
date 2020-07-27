<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="2.0">
    
<xsl:output encoding="UTF-8" method="text" indent="yes"/>
    
    <xsl:template name="name_parser">
        <xsl:param name="text" />
        <xsl:choose>
            <xsl:when test="contains($text, 'CIM_')">
                <xsl:value-of select="substring-before($text,'CIM_')" />
                <xsl:value-of select="''" />
                <xsl:call-template name="name_parser">
                    <xsl:with-param name="text" select="substring-after($text,'CIM_')" />
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="matches($text, '[A-Z]')">
                <xsl:analyze-string regex="^([A-Z]+)([A-Z])([a-z])" select="$text">
                    <xsl:matching-substring><xsl:value-of select="concat(lower-case(regex-group(1)),'_',lower-case(regex-group(2)),regex-group(3))"/></xsl:matching-substring>
                    <xsl:non-matching-substring>
                        <xsl:analyze-string regex="(^[A-Z]+)" select=".">
                            <xsl:matching-substring><xsl:value-of select="lower-case(regex-group(1))"/></xsl:matching-substring>
                            <xsl:non-matching-substring>
                                <xsl:analyze-string regex="([A-Z]+)" select=".">
                                    <xsl:matching-substring><xsl:value-of select="concat('_',lower-case(regex-group(1)))"/></xsl:matching-substring>
                                    <xsl:non-matching-substring><xsl:value-of select="."/>
                                    </xsl:non-matching-substring>
                                </xsl:analyze-string>
                            </xsl:non-matching-substring>
                        </xsl:analyze-string>
                    </xsl:non-matching-substring>          
                </xsl:analyze-string>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$text" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="CIM">
SET client_encoding = 'UTF8';
DROP DATABASE cim;       
CREATE DATABASE cim;
\connect cim;
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="CLASS">
CREATE TABLE public.<xsl:call-template name="name_parser"><xsl:with-param name="text" select="./@NAME" /></xsl:call-template> /*
    <xsl:apply-templates/>
);
    </xsl:template>
    
    <xsl:template match="QUALIFIER">
        <xsl:if test="name(parent::*)='CLASS'">
            <xsl:if test="./@NAME='Description'">
<xsl:value-of select="./VALUE"/> */
(  
    id SERIAL PRIMARY KEY
            </xsl:if>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="PROPERTY">
        , <xsl:call-template name="name_parser"><xsl:with-param name="text" select="./@NAME" /></xsl:call-template> text[]
    </xsl:template>
    
    <xsl:template match="PROPERTY.REFERENCE">
        , <xsl:call-template name="name_parser"><xsl:with-param name="text" select="./@REFERENCECLASS" /></xsl:call-template>_id<xsl:value-of select="count(preceding-sibling::*)+1"/> INTEGER REFERENCES <xsl:call-template name="name_parser"><xsl:with-param name="text" select="./@REFERENCECLASS" /></xsl:call-template>(id)
    </xsl:template>
    
   
</xsl:stylesheet>
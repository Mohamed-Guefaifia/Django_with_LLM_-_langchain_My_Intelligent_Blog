from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
import re


def logo_generator_home(request):
    """Vue principale du générateur de logos"""
    return render(request, 'logo_generator/index.html')


def generate_logo_svg(request):
    """Génère un logo SVG basé sur les paramètres fournis"""
    if request.method == 'POST':
        # Récupérer les paramètres du logo
        data = json.loads(request.body)
        
        logo_type = data.get('type', 'modern')
        text = data.get('text', 'Mon Logo')
        font_size = data.get('font_size', 24)
        primary_color = data.get('primary_color', '#3498db')
        secondary_color = data.get('secondary_color', '#2c3e50')
        background_color = data.get('background_color', '#ffffff')
        width = data.get('width', 300)
        height = data.get('height', 100)
        style = data.get('style', 'clean')
        
        # Nettoyer le texte
        text = re.sub(r'[<>&"]', '', text)[:50]  # Sécurité
        
        # Générer le SVG selon le type
        if logo_type == 'modern':
            svg_content = generate_modern_logo(text, font_size, primary_color, secondary_color, background_color, width, height, style)
        elif logo_type == 'badge':
            svg_content = generate_badge_logo(text, font_size, primary_color, secondary_color, background_color, width, height)
        elif logo_type == 'minimal':
            svg_content = generate_minimal_logo(text, font_size, primary_color, width, height)
        else:
            svg_content = generate_modern_logo(text, font_size, primary_color, secondary_color, background_color, width, height, style)
        
        return HttpResponse(svg_content, content_type='image/svg+xml')
    
    return HttpResponse('Méthode non autorisée', status=405)


def generate_modern_logo(text, font_size, primary_color, secondary_color, bg_color, width, height, style):
    """Génère un logo moderne avec des éléments géométriques"""
    
    # Calculer la taille de police adaptée
    font_size = min(font_size, height * 0.4)
    
    # Créer des éléments décoratifs selon le style
    decorative_elements = ""
    
    if style == 'geometric':
        decorative_elements = f"""
        <rect x="10" y="{height//2 - 15}" width="30" height="30" fill="{primary_color}" rx="5"/>
        <circle cx="25" cy="{height//2}" r="8" fill="{bg_color}"/>
        """
    elif style == 'gradient':
        decorative_elements = f"""
        <defs>
            <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:{primary_color};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{secondary_color};stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect x="0" y="0" width="{width}" height="{height}" fill="url(#logoGrad)" opacity="0.1" rx="10"/>
        """
    elif style == 'tech':
        decorative_elements = f"""
        <polygon points="10,{height//2-10} 30,{height//2-10} 35,{height//2} 30,{height//2+10} 10,{height//2+10}" fill="{primary_color}"/>
        <rect x="15" y="{height//2-5}" width="15" height="10" fill="{bg_color}"/>
        """
    
    svg = f'''
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="{bg_color}" rx="10"/>
        {decorative_elements}
        <text x="{50 if style in ['geometric', 'tech'] else width//2}" y="{height//2 + font_size//3}" 
              font-family="Arial, sans-serif" font-size="{font_size}" 
              fill="{secondary_color}" text-anchor="{'start' if style in ['geometric', 'tech'] else 'middle'}" 
              font-weight="bold">{text}</text>
    </svg>
    '''
    return svg


def generate_badge_logo(text, font_size, primary_color, secondary_color, bg_color, width, height):
    """Génère un logo style badge/emblème"""
    
    font_size = min(font_size, height * 0.3)
    
    svg = f'''
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="badgeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{primary_color};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{secondary_color};stop-opacity:1" />
            </linearGradient>
        </defs>
        
        <!-- Badge principal -->
        <ellipse cx="{width//2}" cy="{height//2}" rx="{width//2 - 10}" ry="{height//2 - 10}" 
                 fill="url(#badgeGrad)" stroke="{secondary_color}" stroke-width="3"/>
        
        <!-- Cercle intérieur -->
        <ellipse cx="{width//2}" cy="{height//2}" rx="{width//2 - 20}" ry="{height//2 - 20}" 
                 fill="none" stroke="{bg_color}" stroke-width="2"/>
        
        <!-- Texte -->
        <text x="{width//2}" y="{height//2 + font_size//3}" 
              font-family="serif" font-size="{font_size}" 
              fill="{bg_color}" text-anchor="middle" 
              font-weight="bold">{text}</text>
    </svg>
    '''
    return svg


def generate_minimal_logo(text, font_size, primary_color, width, height):
    """Génère un logo minimaliste"""
    
    font_size = min(font_size, height * 0.5)
    
    svg = f'''
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
        <!-- Ligne décorative -->
        <line x1="20" y1="{height//2}" x2="{width-20}" y2="{height//2}" 
              stroke="{primary_color}" stroke-width="2"/>
        
        <!-- Points décoratifs -->
        <circle cx="20" cy="{height//2}" r="4" fill="{primary_color}"/>
        <circle cx="{width-20}" cy="{height//2}" r="4" fill="{primary_color}"/>
        
        <!-- Texte -->
        <text x="{width//2}" y="{height//2 - 10}" 
              font-family="Arial, sans-serif" font-size="{font_size}" 
              fill="{primary_color}" text-anchor="middle" 
              font-weight="300">{text}</text>
    </svg>
    '''
    return svg


def download_logo(request):
    """Permet de télécharger le logo généré"""
    if request.method == 'POST':
        svg_content = request.POST.get('svg_content', '')
        filename = request.POST.get('filename', 'logo.svg')
        
        response = HttpResponse(svg_content, content_type='image/svg+xml')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse('Méthode non autorisée', status=405)

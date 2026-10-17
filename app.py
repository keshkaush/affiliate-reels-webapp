import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from dotenv import load_dotenv

from config import Config
from models import Base, Content, AffiliateProgram, ProductAffiliateLink
from omniroute_ai import OmnirouteAI

# --- Copying original project's modules ---
# This is a simplification. In a real project, these would be proper packages
# or shared via a mono-repo setup. For this PoC, we'll copy them.
# Original project path: C:\Users\kesha\projects\affiliate-reels-automation
original_project_path = Path("C:\\Users\\kesha\\projects\\affiliate-reels-automation")
current_project_path = Path(__file__).parent

# Add the original src and scripts directories to the Python path
# This allows direct import of modules like TrendHunter, AffiliateManager, etc.
sys.path.insert(0, str(original_project_path / 'src'))

# Import modules from the original project
from trend_hunter import TrendHunter
from affiliate_manager import AffiliateManager
from social_bot import SocialBot
from dm_handler import DMHandler

# --- Flask App Initialization ---
app = Flask(__name__)
app.config.from_object(Config)
load_dotenv() # Load environment variables from .env

# --- Database Initialization ---
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine) # Create tables if they don't exist
Session = sessionmaker(bind=engine)

# --- AI Service Initialization ---
# Ensure GEMINI_API_KEY is set in .env
try:
    omniroute_ai = OmnirouteAI()
except ValueError as e:
    print(f"Error initializing OmnirouteAI: {e}")
    omniroute_ai = None # Handle gracefully if API key is missing

# --- Original Project Class Instances ---
# These will use our OmnirouteAI for AI-related tasks
trend_hunter = TrendHunter() # Will need to modify TrendHunter to use omniroute_ai
affiliate_manager = AffiliateManager()
social_bot = SocialBot() # Will need to modify SocialBot to use omniroute_ai
dm_handler = DMHandler() # Will need to modify DMHandler to use omniroute_ai

@app.route('/')
def index():
    session = Session()
    all_content = session.query(Content).order_by(desc(Content.timestamp)).all()
    session.close()
    return render_template('index.html', content_list=all_content)

@app.route('/discover_content', methods=['POST'])
def discover_content():
    if omniroute_ai is None:
        flash("AI service not initialized. Please ensure GEMINI_API_KEY is set.", "error")
        return redirect(url_for('index'))

    niche = request.form.get('niche', 'gadgets')
    limit = int(request.form.get('limit', 5))

    flash(f"Starting content discovery for niche: {niche}, limit: {limit}...", "info")

    # Simulate scraping and AI analysis using the original TrendHunter module
    # and our OmnirouteAI wrapper.
    # NOTE: The TrendHunter in the original project directly calls `scraper.py` and `ai_analyzer.py`
    # We would need to modify those to inject our omniroute_ai instance.
    # For this PoC, we'll simulate the integration here.

    # Example: Replace this with actual TrendHunter.find_trending call
    # and integrate omniroute_ai within TrendHunter's AI calls.
    # This part requires deeper integration into the original project's files.
    # For now, let's mock the output for demonstration.
    mock_trends = [
        {'platform': 'instagram', 'video_url': 'https://instagram.com/reel/mock1', 'title': 'Cool Wireless Earbuds #gadget', 'description': 'Listen to music on the go!', 'author': 'mock_user1', 'views': 150000, 'likes': 10000, 'shares': 500, 'comments': 200, 'niche': 'gadgets'},
        {'platform': 'facebook', 'video_url': 'https://facebook.com/watch/?v=mock2', 'title': 'Smart Home Lighting Kit #smarthome', 'description': 'Automate your home lighting.', 'author': 'mock_user2', 'views': 200000, 'likes': 15000, 'shares': 700, 'comments': 300, 'niche': 'gadgets'},
    ]

    session = Session()
    new_content_count = 0
    for trend in mock_trends:
        # Simulate AI analysis
        ai_analysis = omniroute_ai.analyze_video(trend)

        # Check if content already exists to avoid duplicates
        existing_content = session.query(Content).filter_by(video_url=trend['video_url']).first()

        if not existing_content:
            content = Content(
                platform=trend['platform'],
                video_url=trend['video_url'],
                title=trend['title'],
                description=trend['description'],
                author=trend['author'],
                views=trend['views'],
                likes=trend['likes'],
                shares=trend['shares'],
                comments=trend['comments'],
                niche=trend['niche'],
                is_faceless=ai_analysis['is_faceless'],
                products_found=", ".join(ai_analysis['products_found'])
            )
            session.add(content)
            new_content_count += 1
    session.commit()
    session.close()

    flash(f"Discovery complete. Added {new_content_count} new content items.", "success")
    return redirect(url_for('index'))

@app.route('/content/<int:content_id>')
def view_content(content_id):
    session = Session()
    content = session.query(Content).get(content_id)
    if not content:
        flash("Content not found.", "error")
        session.close()
        return redirect(url_for('index'))

    # Find affiliate options for products found in this content
    affiliate_options = []
    products = [p.strip() for p in content.products_found.split(',')] if content.products_found else []

    for product_name in products:
        if product_name:
            # Search in our DB first
            db_links = session.query(ProductAffiliateLink).filter_by(product_name=product_name).all()
            if db_links:
                affiliate_options.append({'product': product_name, 'links': db_links, 'source': 'database'})
            else:
                # Flag for user to provide
                affiliate_options.append({'product': product_name, 'links': [], 'source': 'flagged_for_user'})
    session.close()

    return render_template('content_detail.html', content=content, affiliate_options=affiliate_options)

@app.route('/add_affiliate_link/<int:content_id>/<product_name>', methods=['GET', 'POST'])
def add_affiliate_link(content_id, product_name):
    session = Session()
    content = session.query(Content).get(content_id)
    if not content:
        flash("Content not found.", "error")
        session.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        affiliate_link_url = request.form['affiliate_link_url']
        network = request.form['network']
        commission = request.form.get('commission', 'Unknown')
        cookie_duration = int(request.form.get('cookie_duration', 30))

        # Find or create affiliate program
        aff_program = session.query(AffiliateProgram).filter_by(network=network).first()
        if not aff_program:
            # Simulate priority score calculation (can be more complex with AI)
            priority_score = (float(commission.replace('%','')) * 0.4 if commission != 'Unknown' else 2) + \
                             (cookie_duration / 30) * 0.2 + 0.1 # Simplified
            aff_program = AffiliateProgram(network=network, name=network.capitalize(),
                                           commission_rate=commission, cookie_duration=cookie_duration,
                                           priority_score=round(priority_score, 2))
            session.add(aff_program)
            session.commit() # Commit to get program ID

        new_link = ProductAffiliateLink(
            product_name=product_name,
            affiliate_link=affiliate_link_url,
            content_id=content.id,
            affiliate_program_id=aff_program.id,
            added_by_user=True
        )
        session.add(new_link)
        session.commit()
        flash(f"Affiliate link for {product_name} added successfully!", "success")
        session.close()
        return redirect(url_for('view_content', content_id=content_id))

    session.close()
    return render_template('add_affiliate_link.html', content=content, product_name=product_name)

@app.route('/affiliate_programs')
def list_affiliate_programs():
    session = Session()
    programs = session.query(AffiliateProgram).all()
    session.close()
    return render_template('affiliate_programs.html', programs=programs)

@app.route('/product_affiliate_links')
def list_product_affiliate_links():
    session = Session()
    links = session.query(ProductAffiliateLink).all()
    session.close()
    return render_template('product_affiliate_links.html', links=links)

if __name__ == '__main__':
    app.run(debug=True)
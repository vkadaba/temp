import React, { useEffect, useState } from 'react';
import '@/App.css';
import axios from 'axios';
import { Phone, Mail, MapPin, ChevronRight, Award, Users, Wrench, CheckCircle, ExternalLink, Play, Menu, X } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const OEM_LOGOS = {
  'Mycronic':           'https://www.mycronic.com/siteassets/mycronic-logo.svg',
  'Graco':              'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Graco_logo.svg/320px-Graco_logo.svg.png',
  'AccoTEST Global':    'https://accotest.com/wp-content/uploads/2021/08/accotest-logo.png',
  'JHT Semiconductors': 'https://jhtsemiconductor.com/wp-content/uploads/2022/03/JHT-logo.png',
  'PVA TePla AS':       'https://www.pvatepla-sam.com/wp-content/uploads/2020/08/logo-pva-tepla-as.png',
};

const CATEGORY_VISUALS = {
  'Electronic Assembly Products': {
    icon: '🔌',
    gradient: 'from-blue-700 to-blue-900',
    highlights: ['Pick & Place Machines', 'Reflow Ovens', 'Screen Printers', 'Wave Soldering'],
  },
  'Assembly Tools': {
    icon: '🔧',
    gradient: 'from-indigo-700 to-indigo-900',
    highlights: ['BGA Rework Systems', 'Robotic Soldering', 'Vapor Phase Soldering', 'Workbenches'],
  },
  'Inspection and Testing': {
    icon: '🔬',
    gradient: 'from-cyan-700 to-cyan-900',
    highlights: ['X-Ray Inspection', '3D AOI Systems', 'Flying Probe Testers', 'Thermal Profilers'],
  },
  'Semiconductor': {
    icon: '🔲',
    gradient: 'from-violet-700 to-violet-900',
    highlights: ['Test Handlers', 'Functional Testers', 'Plasma Cleaners', 'Die Bonders'],
  },
  'Non Destructive Testing': {
    icon: '📡',
    gradient: 'from-teal-700 to-teal-900',
    highlights: ['Scanning Acoustic Microscopy', 'Warpage Measurement', 'Subsurface Analysis', 'Material Characterisation'],
  },
  'Mechanical': {
    icon: '⚙️',
    gradient: 'from-slate-600 to-slate-800',
    highlights: ['CNC Machining Centres', 'PCB Routing Machines', 'PCB Depanelling', 'Solder Paste Mixers'],
  },
};

function App() {
  const [partnerships, setPartnerships] = useState([]);
  const [products, setProducts] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [categoryProducts, setCategoryProducts] = useState([]);
  const [contactForm, setContactForm] = useState({ name: '', email: '', phone: '', company: '', message: '' });
  const [submitStatus, setSubmitStatus] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => { fetchData(); }, []);

  useEffect(() => {
    const handleScroll = () => setMobileMenuOpen(false);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const fetchData = async () => {
    try {
      const [pRes, prRes, tRes] = await Promise.all([
        axios.get(`${API}/partnerships`),
        axios.get(`${API}/products`),
        axios.get(`${API}/testimonials`),
      ]);
      setPartnerships(pRes.data);
      setProducts(prRes.data);
      setTestimonials(tRes.data);
    } catch (err) { console.error('Error fetching data:', err); }
  };

  const handleContactSubmit = async (e) => {
    e.preventDefault();
    setSubmitStatus('sending');
    try {
      await axios.post(`${API}/contact`, contactForm);
      setSubmitStatus('success');
      setContactForm({ name: '', email: '', phone: '', company: '', message: '' });
      setTimeout(() => setSubmitStatus(''), 3000);
    } catch {
      setSubmitStatus('error');
      setTimeout(() => setSubmitStatus(''), 3000);
    }
  };

  const handleCategoryClick = async (name) => {
    setSelectedCategory(name);
    try {
      const res = await axios.get(`${API}/products?category=${encodeURIComponent(name)}`);
      setCategoryProducts(res.data);
    } catch (err) { console.error(err); }
  };

  const closeModal = () => { setSelectedCategory(null); setCategoryProducts([]); };

  const countByCategory = (name) => products.filter(p => p.category === name).length;

  const navLinks = ['About', 'Products', 'Partnerships', 'Testimonials', 'Contact'];

  const clientLogos = [
    { name: 'ABB Group',          src: 'https://www.accurexsolutions.com/img/client-logo/abb.png' },
    { name: 'Aplab Limited',      src: 'https://www.accurexsolutions.com/img/client-logo/aplab.png' },
    { name: 'Bharat Electronics', src: 'https://www.accurexsolutions.com/img/client-logo/bel.png' },
    { name: 'BHEL',               src: 'https://www.accurexsolutions.com/img/client-logo/bhel.png' },
    { name: 'HCL',                src: 'https://www.accurexsolutions.com/img/client-logo/hcl.png' },
    { name: 'Tata Group',         src: 'https://www.accurexsolutions.com/img/client-logo/tata.png' },
    { name: 'DRDO',               src: 'https://www.accurexsolutions.com/img/client-logo/drdo.png' },
    { name: 'Intel',              src: 'https://www.accurexsolutions.com/img/client-logo/intel.png' },
  ];

  const getEmbedUrl = (url) => {
    if (!url || url === 'PLACEHOLDER_FOR_VIDEO_URL') return null;
    const yt = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\s]+)/);
    if (yt) return `https://www.youtube.com/embed/${yt[1]}`;
    const vm = url.match(/vimeo\.com\/(\d+)/);
    if (vm) return `https://player.vimeo.com/video/${vm[1]}`;
    return url;
  };

  const videoTestimonials = testimonials.filter(t => t.video_url && t.video_url !== 'PLACEHOLDER_FOR_VIDEO_URL');
  const hasPlaceholderVideo = testimonials.some(t => t.video_url === 'PLACEHOLDER_FOR_VIDEO_URL');
  const textTestimonials = testimonials.filter(t => t.testimonial_text && t.testimonial_text !== 'Video testimonial from demo center inauguration');

  return (
    <div className="min-h-screen bg-white" data-testid="accurex-website">

      {/* ── Navigation ── */}
      <nav className="bg-white shadow-md sticky top-0 z-50" data-testid="main-navigation">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <img src="https://customer-assets.emergentagent.com/job_accurex-refresh/artifacts/ztq8i08p_Accurex_Logo.png" alt="Accurex Solutions" className="h-10 w-auto" />
            <div className="hidden md:flex space-x-8">
              {navLinks.map(l => <a key={l} href={`#${l.toLowerCase()}`} className="text-gray-700 hover:text-[#1B3C9B] transition font-medium">{l}</a>)}
            </div>
            {/* FIX #1 — Hamburger */}
            <button className="md:hidden p-2 rounded-md text-gray-700 hover:text-[#1B3C9B] hover:bg-gray-100 transition" onClick={() => setMobileMenuOpen(!mobileMenuOpen)} aria-label="Toggle menu" data-testid="mobile-menu-toggle">
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
        {mobileMenuOpen && (
          <div className="md:hidden bg-white border-t border-gray-100 shadow-lg" data-testid="mobile-menu">
            <div className="px-4 py-3 space-y-1">
              {navLinks.map(l => (
                <a key={l} href={`#${l.toLowerCase()}`} onClick={() => setMobileMenuOpen(false)} className="block px-4 py-3 rounded-lg text-gray-700 hover:text-[#1B3C9B] hover:bg-blue-50 font-medium transition">{l}</a>
              ))}
            </div>
          </div>
        )}
      </nav>

      {/* ── Hero ── */}
      <section className="relative bg-gradient-to-r from-[#1B3C9B] via-[#2046A4] to-[#1B3C9B] text-white py-20" data-testid="hero-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-block bg-white text-[#1B3C9B] px-6 py-3 rounded-lg font-bold text-xl mb-6 shadow-lg" data-testid="years-badge">
                🎉 Celebrating 39 Years of Excellence
              </div>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">Fulfilling Our Promise to Electronic Assembly Houses</h1>
              <p className="text-xl mb-8 text-blue-100">Since 1987, Accurex Solutions has been a trusted partner for electronics manufacturing across EMS, automotive, defense, aerospace, and semiconductor sectors.</p>
              <div className="flex flex-wrap gap-4">
                <a href="#contact" className="bg-white text-[#1B3C9B] px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition shadow-lg" data-testid="cta-contact">Get In Touch</a>
                <a href="#products" className="bg-white/10 backdrop-blur-sm text-white border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white/20 transition" data-testid="cta-products">View Products</a>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
                {/* FIX #6 — consistent stats */}
                <div className="grid grid-cols-2 gap-6">
                  <div className="text-center"><Award className="w-12 h-12 mx-auto mb-2" /><div className="text-3xl font-bold">39</div><div className="text-sm text-blue-200">Years Experience</div></div>
                  <div className="text-center"><Users className="w-12 h-12 mx-auto mb-2" /><div className="text-3xl font-bold">2000+</div><div className="text-sm text-blue-200">Satisfied Customers</div></div>
                  <div className="text-center"><Wrench className="w-12 h-12 mx-auto mb-2" /><div className="text-3xl font-bold">5400+</div><div className="text-sm text-blue-200">Equipment Installed</div></div>
                  <div className="text-center"><CheckCircle className="w-12 h-12 mx-auto mb-2" /><div className="text-3xl font-bold">24/7</div><div className="text-sm text-blue-200">Support</div></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── About ── */}
      <section id="about" className="py-16 bg-gray-50" data-testid="about-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Welcome to Accurex Solutions</h2>
            <div className="w-24 h-1 bg-[#1B3C9B] mx-auto mb-6"></div>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">
              Since <strong>1987</strong>, Accurex Solutions Pvt. Ltd., Bengaluru, has been a <strong>trusted partner for electronics manufacturing</strong> across EMS, automotive, defense, aerospace, and semiconductor sectors. We provide <strong>end-to-end manufacturing solutions</strong> covering pick & place, solder paste printing, multi-zone reflow, wave/selective soldering, 3D inspection, AOI, and X-ray systems. For <strong>semiconductor OSAT</strong>, we supply process equipment, testing equipment, inspection and reliability tools. With <strong>2000+ satisfied customers</strong> and pan-India presence, we deliver purpose-built solutions with a <strong>100% Customer Satisfaction Guarantee.</strong>
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[['🎯','Customised Testing Solutions','Tailored ATE and test fixtures designed specifically for your manufacturing needs'],
              ['⚡','24x7 Support','Factory-trained engineers providing consistent after-sales service support'],
              ['🏭','Turnkey Solutions','Complete SMT line equipment from PCB loader to unloader']
            ].map(([icon, title, desc]) => (
              <div key={title} className="bg-white p-6 rounded-lg shadow-lg border-t-4 border-[#1B3C9B]">
                <div className="text-[#1B3C9B] text-4xl mb-4">{icon}</div>
                <h3 className="text-xl font-bold mb-3 text-gray-900">{title}</h3>
                <p className="text-gray-600">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FIX #2: Products — visual cards, no placeholder ── */}
      <section id="products" className="py-16 bg-white" data-testid="products-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Product Categories</h2>
            <div className="w-24 h-1 bg-[#1B3C9B] mx-auto mb-6"></div>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">
              Comprehensive solutions for <strong>PCB assembly</strong>, <strong>semiconductor testing</strong>, <strong>inspection equipment</strong>, and <strong>electronic manufacturing</strong>
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {Object.entries(CATEGORY_VISUALS).map(([title, vis], index) => {
              const count = countByCategory(title);
              return (
                <div key={index} onClick={() => handleCategoryClick(title)}
                  className="group bg-white rounded-xl overflow-hidden border-2 border-gray-100 hover:border-[#1B3C9B] hover:shadow-2xl transition-all duration-300 cursor-pointer transform hover:-translate-y-1"
                  data-testid={`product-category-${index}`}>
                  {/* Gradient header */}
                  <div className={`h-36 bg-gradient-to-br ${vis.gradient} flex items-center justify-center relative`}>
                    <span className="text-6xl drop-shadow-lg">{vis.icon}</span>
                    {count > 0 && (
                      <div className="absolute top-3 right-3 bg-white/90 text-gray-800 text-xs font-bold px-2 py-1 rounded-full shadow">
                        {count} products
                      </div>
                    )}
                  </div>
                  {/* Card body */}
                  <div className="p-6">
                    <h3 className="text-xl font-bold mb-3 text-[#1B3C9B]">{title}</h3>
                    <ul className="space-y-1.5 mb-4">
                      {vis.highlights.map((h, i) => (
                        <li key={i} className="text-sm text-gray-600 flex items-center gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-[#1B3C9B] flex-shrink-0" />
                          {h}
                        </li>
                      ))}
                    </ul>
                    <div className="flex items-center text-[#1B3C9B] font-semibold text-sm">
                      Explore Products <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── FIX #5: Partnerships with logos ── */}
      <section id="partnerships" className="py-16 bg-gradient-to-br from-blue-50 to-white" data-testid="partnerships-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our OEM Partnerships</h2>
            <div className="w-24 h-1 bg-[#1B3C9B] mx-auto mb-6"></div>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">Strategic partnerships with global leaders in <strong>electronics manufacturing equipment</strong> and <strong>semiconductor testing solutions</strong></p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {partnerships.map((p, index) => (
              <div key={p.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 border border-gray-100" data-testid={`partnership-${index}`}>
                {p.partnership_date === '2025' && (
                  <div className="bg-green-500 text-white text-xs font-bold text-center py-1.5 tracking-wide">🆕 NEW PARTNERSHIP 2025</div>
                )}
                <div className="p-6">
                  {/* Logo with graceful fallback */}
                  <div className="h-14 flex items-center mb-4">
                    {OEM_LOGOS[p.company_name] ? (
                      <img src={OEM_LOGOS[p.company_name]} alt={p.company_name}
                        className="max-h-10 max-w-[140px] object-contain"
                        onError={(e) => { e.target.style.display='none'; e.target.nextSibling.style.display='block'; }} />
                    ) : null}
                    <span className="text-xl font-bold text-[#1B3C9B]" style={{display: OEM_LOGOS[p.company_name] ? 'none' : 'block'}}>{p.company_name}</span>
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{p.company_name}</h3>
                  <p className="text-gray-600 mb-3 text-sm leading-relaxed">{p.description}</p>
                  {p.products_offered && (
                    <p className="text-xs text-gray-500 mb-4"><span className="font-semibold">Products:</span> {p.products_offered}</p>
                  )}
                  <a href={p.website_url} target="_blank" rel="noopener noreferrer"
                    className="inline-flex items-center text-sm text-[#1B3C9B] font-semibold hover:underline transition">
                    Visit Website <ExternalLink className="w-3.5 h-3.5 ml-1.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FIX #3: Testimonials with real video embed logic ── */}
      <section id="testimonials" className="py-16 bg-white" data-testid="testimonials-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">What Our Clients Say</h2>
            <div className="w-24 h-1 bg-[#1B3C9B] mx-auto mb-6"></div>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">Trusted by leading companies in <strong>aerospace</strong>, <strong>defense electronics</strong>, <strong>consumer electronics</strong>, and <strong>medical device manufacturing</strong></p>
          </div>

          {/* Real video embeds */}
          {videoTestimonials.map((t, i) => (
            <div key={i} className="mb-12 bg-gradient-to-br from-[#1B3C9B] to-[#2046A4] rounded-xl p-8 shadow-2xl" data-testid="video-testimonial">
              <div className="max-w-4xl mx-auto">
                <h3 className="text-2xl font-bold text-white text-center mb-1">{t.client_name}</h3>
                {t.designation && <p className="text-blue-200 text-center text-sm mb-6">{t.designation}</p>}
                <div className="relative rounded-xl overflow-hidden" style={{paddingTop:'56.25%'}}>
                  <iframe src={getEmbedUrl(t.video_url)} className="absolute inset-0 w-full h-full" frameBorder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen title={`${t.client_name} testimonial`} />
                </div>
              </div>
            </div>
          ))}

          {/* Clean placeholder (no "upload area" text) */}
          {hasPlaceholderVideo && (
            <div className="mb-12 bg-gradient-to-br from-[#1B3C9B] to-[#2046A4] rounded-xl p-8 shadow-2xl" data-testid="video-testimonial-placeholder">
              <div className="max-w-4xl mx-auto text-center">
                <div className="bg-black/20 rounded-xl p-10 border border-white/20">
                  <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <Play className="w-10 h-10 text-white ml-1" />
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-2">Mr. Chan Wha Pak</h3>
                  <p className="text-blue-200 text-sm">Distinguished Guest — Demo Centre Inauguration</p>
                  <p className="text-blue-300/70 text-xs mt-4">Video coming soon</p>
                </div>
              </div>
            </div>
          )}

          {/* Text testimonials */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {textTestimonials.map((t, index) => (
              <div key={t.id} className="bg-gray-50 p-6 rounded-xl shadow-md border border-gray-100" data-testid={`testimonial-${index}`}>
                <div className="text-[#1B3C9B] text-4xl font-serif mb-3">"</div>
                <p className="text-gray-700 mb-4 italic leading-relaxed">{t.testimonial_text}</p>
                <div className="border-t border-gray-200 pt-4">
                  <p className="font-semibold text-gray-900">{t.client_name}</p>
                  {t.company_name && <p className="text-sm text-gray-500">{t.company_name}</p>}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Clients ── */}
      <section className="py-16 bg-gray-50" data-testid="clients-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Valued Clients</h2>
            <div className="w-24 h-1 bg-[#1B3C9B] mx-auto mb-6"></div>
            <p className="text-lg text-gray-700">Trusted by over 2000+ leading organisations across India</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center">
            {clientLogos.map((client, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition flex items-center justify-center" data-testid={`client-logo-${index}`}>
                <img src={client.src} alt={client.name} className="max-h-16 w-auto grayscale hover:grayscale-0 transition duration-300" />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Contact ── */}
      <section id="contact" className="py-16 bg-gradient-to-br from-[#1B3C9B] to-[#2046A4] text-white" data-testid="contact-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Get In Touch</h2>
            <div className="w-24 h-1 bg-white mx-auto mb-6"></div>
            <p className="text-xl text-blue-100">One passion, One Goal — Let's work together!</p>
          </div>
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-bold mb-6">Contact Information</h3>
              <div className="space-y-4">
                {[[MapPin,'Address','Accurex Solutions Pvt. Ltd.\nBengaluru, Karnataka, India'],
                  [Phone,'Phone','24x7 Support Available'],
                  [Mail,'Email','info@accurexsolutions.com']
                ].map(([Icon, label, val]) => (
                  <div key={label} className="flex items-start">
                    <Icon className="w-6 h-6 mr-4 mt-1 flex-shrink-0" />
                    <div><p className="font-semibold">{label}</p><p className="text-blue-100">{val}</p></div>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <form onSubmit={handleContactSubmit} className="space-y-4" data-testid="contact-form">
                <input type="text" placeholder="Your Name *" required value={contactForm.name} onChange={e => setContactForm({...contactForm, name: e.target.value})} className="w-full px-4 py-3 rounded-lg text-gray-900" data-testid="contact-name" />
                <input type="email" placeholder="Your Email *" required value={contactForm.email} onChange={e => setContactForm({...contactForm, email: e.target.value})} className="w-full px-4 py-3 rounded-lg text-gray-900" data-testid="contact-email" />
                <input type="tel" placeholder="Phone Number" value={contactForm.phone} onChange={e => setContactForm({...contactForm, phone: e.target.value})} className="w-full px-4 py-3 rounded-lg text-gray-900" data-testid="contact-phone" />
                <input type="text" placeholder="Company Name" value={contactForm.company} onChange={e => setContactForm({...contactForm, company: e.target.value})} className="w-full px-4 py-3 rounded-lg text-gray-900" data-testid="contact-company" />
                <textarea placeholder="Your Message *" required rows="4" value={contactForm.message} onChange={e => setContactForm({...contactForm, message: e.target.value})} className="w-full px-4 py-3 rounded-lg text-gray-900" data-testid="contact-message" />
                <button type="submit" disabled={submitStatus === 'sending'} className="w-full bg-yellow-400 text-blue-900 px-8 py-3 rounded-lg font-semibold hover:bg-yellow-300 transition disabled:opacity-50" data-testid="contact-submit">
                  {submitStatus === 'sending' ? 'Sending…' : 'Send Message'}
                </button>
                {submitStatus === 'success' && <p className="text-green-400 text-center">Message sent successfully!</p>}
                {submitStatus === 'error' && <p className="text-red-400 text-center">Error sending message. Please try again.</p>}
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* ── FIX #4: Footer — clean 3-column layout, keywords hidden via sr-only ── */}
      <footer className="bg-gray-900 text-white py-10" data-testid="footer">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8 mb-8">
            <div>
              <img src="https://customer-assets.emergentagent.com/job_accurex-refresh/artifacts/ztq8i08p_Accurex_Logo.png" alt="Accurex Solutions" className="h-8 w-auto mb-3 brightness-0 invert" />
              <p className="text-gray-400 text-sm">39 years of trusted excellence in electronics manufacturing equipment across India.</p>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">Quick Links</h4>
              <ul className="space-y-2">
                {navLinks.map(l => <li key={l}><a href={`#${l.toLowerCase()}`} className="text-gray-400 hover:text-white text-sm transition">{l}</a></li>)}
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">Contact</h4>
              <p className="text-gray-400 text-sm">Bengaluru, Karnataka, India</p>
              <p className="text-gray-400 text-sm mt-1">info@accurexsolutions.com</p>
              <p className="text-gray-400 text-sm mt-1">24x7 Support Available</p>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-6 text-center">
            <p className="text-gray-500 text-sm">© 1987 – 2025 Accurex Solutions Pvt. Ltd. · All rights reserved</p>
          </div>
          {/* SEO keywords — invisible to users, readable by crawlers */}
          <div className="sr-only">SMT Equipment India · PCB Assembly Solutions · Semiconductor Testing · Automatic Test Equipment · Electronic Manufacturing Services · Pick and Place Machines · Reflow Ovens · X-Ray Inspection · AOI Systems · Capital Equipment · Bengaluru · Karnataka</div>
        </div>
      </footer>

      {/* ── Product Modal ── */}
      {selectedCategory && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={closeModal}>
          <div className="bg-white rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className={`bg-gradient-to-r ${CATEGORY_VISUALS[selectedCategory]?.gradient || 'from-[#1B3C9B] to-[#2046A4]'} text-white p-6 flex justify-between items-center`}>
              <div>
                <h2 className="text-3xl font-bold mb-1">{selectedCategory}</h2>
                <p className="text-white/80 text-sm">{categoryProducts.length} Products Available</p>
              </div>
              <button onClick={closeModal} className="text-white hover:bg-white/20 rounded-full p-2 transition"><X className="w-6 h-6" /></button>
            </div>
            <div className="overflow-y-auto max-h-[calc(90vh-120px)] p-6">
              {categoryProducts.length === 0 ? (
                <div className="text-center py-12 text-gray-400">
                  <p className="text-lg">Detailed product list coming soon.</p>
                  <p className="text-sm mt-2">Contact us for full specifications.</p>
                </div>
              ) : (
                <div className="grid md:grid-cols-2 gap-6">
                  {categoryProducts.map(product => (
                    <div key={product.id} className="bg-gray-50 rounded-xl p-6 border-2 border-gray-100 hover:border-[#1B3C9B] hover:shadow-lg transition">
                      {product.is_featured && (
                        <div className="inline-block bg-[#1B3C9B]/10 text-[#1B3C9B] px-3 py-1 rounded-full text-xs font-bold border border-[#1B3C9B]/30 mb-3">⭐ FEATURED</div>
                      )}
                      <h3 className="text-xl font-bold text-[#1B3C9B] mb-2">{product.name}</h3>
                      {product.manufacturer && (
                        <div className="text-xs text-gray-600 font-semibold mb-3 bg-white border border-gray-200 px-3 py-1 rounded-full inline-block">🏭 {product.manufacturer}</div>
                      )}
                      <p className="text-gray-600 mb-4 text-sm leading-relaxed">{product.description}</p>
                      {product.features?.length > 0 && (
                        <ul className="space-y-1">
                          {product.features.slice(0, 4).map((f, i) => (
                            <li key={i} className="text-xs text-gray-600 flex items-start">
                              <CheckCircle className="w-4 h-4 text-[#1B3C9B] mr-2 mt-0.5 flex-shrink-0" />{f}
                            </li>
                          ))}
                          {product.features.length > 4 && <li className="text-xs text-gray-400 pl-6">+ {product.features.length - 4} more features</li>}
                        </ul>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

export default App;

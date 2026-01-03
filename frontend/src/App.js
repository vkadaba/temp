import React, { useEffect, useState } from 'react';
import '@/App.css';
import axios from 'axios';
import { Phone, Mail, MapPin, ChevronRight, Award, Users, Wrench, CheckCircle, ExternalLink, Play } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [partnerships, setPartnerships] = useState([]);
  const [products, setProducts] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [categoryProducts, setCategoryProducts] = useState([]);
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    message: ''
  });
  const [submitStatus, setSubmitStatus] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [partnershipsRes, productsRes, testimonialsRes] = await Promise.all([
        axios.get(`${API}/partnerships`),
        axios.get(`${API}/products`),
        axios.get(`${API}/testimonials`)
      ]);
      setPartnerships(partnershipsRes.data);
      setProducts(productsRes.data);
      setTestimonials(testimonialsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleContactSubmit = async (e) => {
    e.preventDefault();
    setSubmitStatus('sending');
    try {
      await axios.post(`${API}/contact`, contactForm);
      setSubmitStatus('success');
      setContactForm({ name: '', email: '', phone: '', company: '', message: '' });
      setTimeout(() => setSubmitStatus(''), 3000);
    } catch (error) {
      console.error('Error submitting form:', error);
      setSubmitStatus('error');
      setTimeout(() => setSubmitStatus(''), 3000);
    }
  };

  const handleCategoryClick = async (categoryName) => {
    setSelectedCategory(categoryName);
    try {
      const response = await axios.get(`${API}/products?category=${encodeURIComponent(categoryName)}`);
      setCategoryProducts(response.data);
    } catch (error) {
      console.error('Error fetching category products:', error);
    }
  };

  const closeProductModal = () => {
    setSelectedCategory(null);
    setCategoryProducts([]);
  };

  const getProductCountByCategory = (categoryName) => {
    return products.filter(p => p.category === categoryName).length;
  };

  const productCategories = [
    {
      title: 'Electronic Assembly Products',
      description: 'PCB loader, Screen printer, Pick and Place, Reflow oven, 3D SPI',
      icon: '🔌'
    },
    {
      title: 'Assembly Tools',
      description: 'Component forming tools, ESD workbench, Soldering stations, BGA rework',
      icon: '🔧'
    },
    {
      title: 'Inspection and Testing',
      description: 'AOI, 3D SPI, X-Ray inspection, Bond tester, Flying probe tester',
      icon: '🔬'
    },
    {
      title: 'Semiconductor',
      description: 'AOI, Manual bonders, Bond tester, Plasma cleaning, X-Ray inspection',
      icon: '🔲'
    },
    {
      title: 'Non Destructive Testing',
      description: 'SAM, Topography measurement, X-Ray inspection',
      icon: '📡'
    },
    {
      title: 'Mechanical',
      description: 'CNC machines, PCB drilling machines, PCB routing machines',
      icon: '⚙️'
    }
  ];

  const clientLogos = [
    { name: 'ABB Group', src: 'https://www.accurexsolutions.com/img/client-logo/abb.png' },
    { name: 'Aplab Limited', src: 'https://www.accurexsolutions.com/img/client-logo/aplab.png' },
    { name: 'Bharat Electronics', src: 'https://www.accurexsolutions.com/img/client-logo/bel.png' },
    { name: 'BHEL', src: 'https://www.accurexsolutions.com/img/client-logo/bhel.png' },
    { name: 'HCL', src: 'https://www.accurexsolutions.com/img/client-logo/hcl.png' },
    { name: 'Tata Group', src: 'https://www.accurexsolutions.com/img/client-logo/tata.png' },
    { name: 'DRDO', src: 'https://www.accurexsolutions.com/img/client-logo/drdo.png' },
    { name: 'Intel', src: 'https://www.accurexsolutions.com/img/client-logo/intel.png' }
  ];

  return (
    <div className="min-h-screen bg-white" data-testid="accurex-website">
      {/* SEO Meta tags handled in index.html */}
      
      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-0 z-50" data-testid="main-navigation">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center">
              <img 
                src="https://customer-assets.emergentagent.com/job_accurex-refresh/artifacts/ztq8i08p_Accurex_Logo.png" 
                alt="Accurex Solutions" 
                className="h-10 w-auto"
              />
            </div>
            <div className="hidden md:flex space-x-8">
              <a href="#about" className="text-gray-700 hover:text-[#1B3C9B] transition font-medium">About</a>
              <a href="#products" className="text-gray-700 hover:text-[#1B3C9B] transition font-medium">Products</a>
              <a href="#partnerships" className="text-gray-700 hover:text-[#1B3C9B] transition font-medium">Partnerships</a>
              <a href="#testimonials" className="text-gray-700 hover:text-[#1B3C9B] transition font-medium">Testimonials</a>
              <a href="#contact" className="text-gray-700 hover:text-[#1B3C9B] transition font-medium">Contact</a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-[#1B3C9B] via-[#2046A4] to-[#1B3C9B] text-white py-20" data-testid="hero-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-block bg-white text-[#1B3C9B] px-6 py-3 rounded-lg font-bold text-xl mb-6 shadow-lg" data-testid="years-badge">
                🎉 Celebrating 39 Years of Excellence
              </div>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
                Fulfilling Our Promise to Electronic Assembly Houses
              </h1>
              <p className="text-xl mb-8 text-blue-100">
                Since 1987, Accurex Solutions has been a trusted partner for electronics manufacturing across EMS, automotive, defense, aerospace, and semiconductor sectors. With 1,500+ satisfied customers and 39 years of industry experience, we deliver 100% customer satisfaction.
              </p>
              <div className="flex flex-wrap gap-4">
                <a href="#contact" className="bg-white text-[#1B3C9B] px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition shadow-lg" data-testid="cta-contact">
                  Get In Touch
                </a>
                <a href="#products" className="bg-white/10 backdrop-blur-sm text-white border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white/20 transition" data-testid="cta-products">
                  View Products
                </a>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
                <div className="grid grid-cols-2 gap-6">
                  <div className="text-center">
                    <Award className="w-12 h-12 mx-auto mb-2 text-white" />
                    <div className="text-3xl font-bold">39</div>
                    <div className="text-sm text-blue-200">Years Industry Experience</div>
                  </div>
                  <div className="text-center">
                    <Users className="w-12 h-12 mx-auto mb-2 text-white" />
                    <div className="text-3xl font-bold">5400+</div>
                    <div className="text-sm text-blue-200">Equipment Installations</div>
                  </div>
                  <div className="text-center">
                    <Wrench className="w-12 h-12 mx-auto mb-2 text-white" />
                    <div className="text-3xl font-bold">24/7</div>
                    <div className="text-sm text-blue-200">Support</div>
                  </div>
                  <div className="text-center">
                    <CheckCircle className="w-12 h-12 mx-auto mb-2 text-white" />
                    <div className="text-3xl font-bold">100%</div>
                    <div className="text-sm text-blue-200">Commitment</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-16 bg-gray-50" data-testid="about-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Welcome to Accurex Solutions</h2>
            <div className="w-24 h-1 bg-[#1B3C9B] mx-auto mb-6"></div>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">
              Since <strong>1987</strong>, Accurex Solutions Pvt. Ltd., Bengaluru, has been a <strong>trusted partner for electronics manufacturing</strong> across EMS, automotive, defense, aerospace, and semiconductor sectors. We provide <strong>end-to-end manufacturing solutions</strong> with an extensive product line covering pick & place, solder paste printing, multi-zone reflow, wave/selective soldering, vapor phase soldering, 3D inspection, AOI, and X-ray systems. For <strong>semiconductor assembly and test (OSAT)</strong>, we supply process equipment, testing equipment, inspection and reliability tools, and specialized custom equipment. With <strong>1,500+ satisfied customers</strong> and pan-India presence, we deliver flexible, purpose-built solutions for defense, aerospace, automotive, and high-mix production environments. <strong>100% Customer Satisfaction Guarantee</strong> is something we strive to achieve with every interaction.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-lg border-t-4 border-[#1B3C9B]">
              <div className="text-[#1B3C9B] text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">Customized Testing Solutions</h3>
              <p className="text-gray-600">Tailored ATE and test fixtures designed specifically for your manufacturing needs</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg border-t-4 border-[#1B3C9B]">
              <div className="text-[#1B3C9B] text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">24x7 Support</h3>
              <p className="text-gray-600">Factory-trained engineers providing consistent after-sales service support</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg border-t-4 border-[#1B3C9B]">
              <div className="text-[#1B3C9B] text-4xl mb-4">🏭</div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">Turnkey Solutions</h3>
              <p className="text-gray-600">Complete SMT line equipment from PCB loader to unloader</p>
            </div>
          </div>
        </div>
      </section>

      {/* Products Section */}
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
            {productCategories.map((category, index) => {
              const productCount = getProductCountByCategory(category.title);
              return (
                <div 
                  key={index} 
                  onClick={() => handleCategoryClick(category.title)}
                  className="bg-white p-6 rounded-lg hover:shadow-xl transition border-2 border-gray-100 hover:border-[#1B3C9B] cursor-pointer transform hover:scale-105" 
                  data-testid={`product-category-${index}`}
                >
                  <div className="text-5xl mb-4">{category.icon}</div>
                  <h3 className="text-xl font-bold mb-3 text-[#1B3C9B]">{category.title}</h3>
                  <p className="text-gray-600 mb-4 text-sm">{category.description}</p>
                  <div className="flex items-center text-[#1B3C9B] font-semibold text-sm">
                    View {productCount} Products <ChevronRight className="w-4 h-4 ml-1" />
                  </div>
                </div>
              );
            })}
          </div>
          
          {/* Image Upload Placeholder */}
          <div className="mt-12 bg-blue-50 border-2 border-dashed border-[#1B3C9B] rounded-lg p-12 text-center" data-testid="product-images-placeholder">
            <div className="text-[#1B3C9B] text-6xl mb-4">📷</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Product Images Section</h3>
            <p className="text-gray-600 mb-4">Upload your product equipment images and updates here</p>
            <div className="inline-block bg-[#1B3C9B] text-white px-6 py-2 rounded-lg">
              Image Upload Area - Coming Soon
            </div>
          </div>
        </div>
      </section>

      {/* OEM Partnerships Section */}
      <section id="partnerships" className="py-16 bg-gradient-to-br from-blue-50 to-white" data-testid="partnerships-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our OEM Partnerships</h2>
            <div className="w-24 h-1 bg-[#1B3C9B] mx-auto mb-6"></div>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">
              Strategic partnerships with global leaders in <strong>electronics manufacturing equipment</strong> and <strong>semiconductor testing solutions</strong>
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {partnerships.map((partnership, index) => (
              <div key={partnership.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition" data-testid={`partnership-${index}`}>
                <div className="p-6">
                  {partnership.partnership_date === '2025' && (
                    <div className="inline-block bg-green-500 text-white px-3 py-1 rounded-full text-sm font-semibold mb-4">
                      🆕 NEW 2025
                    </div>
                  )}
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">{partnership.company_name}</h3>
                  <p className="text-gray-600 mb-4">{partnership.description}</p>
                  {partnership.products_offered && (
                    <div className="mb-4">
                      <span className="font-semibold text-gray-900">Products:</span>
                      <p className="text-sm text-gray-600 mt-1">{partnership.products_offered}</p>
                    </div>
                  )}
                  <a 
                    href={partnership.website_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-[#1B3C9B] font-semibold hover:text-[#2046A4] transition"
                  >
                    Visit Website <ExternalLink className="w-4 h-4 ml-2" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-16 bg-white" data-testid="testimonials-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">What Our Clients Say</h2>
            <div className="w-24 h-1 bg-[#1B3C9B] mx-auto mb-6"></div>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">
              Trusted by leading companies in <strong>aerospace</strong>, <strong>defense electronics</strong>, <strong>consumer electronics</strong>, and <strong>medical device manufacturing</strong>
            </p>
          </div>
          
          {/* Video Testimonial Placeholder */}
          <div className="mb-12 bg-gradient-to-br from-[#1B3C9B] to-[#2046A4] rounded-xl p-8 shadow-2xl" data-testid="video-testimonial-placeholder">
            <div className="max-w-4xl mx-auto">
              <div className="bg-black/20 backdrop-blur-sm rounded-lg p-12 text-center border-2 border-white/30">
                <Play className="w-24 h-24 mx-auto mb-6 text-white" />
                <h3 className="text-3xl font-bold text-white mb-3">Featured Video Testimonial</h3>
                <p className="text-xl text-blue-100 mb-4">
                  Mr. Chan Wha Pak - Demo Center Inauguration Speech
                </p>
                <div className="inline-block bg-white text-[#1B3C9B] px-6 py-3 rounded-lg font-semibold">
                  📹 Video Upload Area - Add your video URL here
                </div>
              </div>
            </div>
          </div>

          {/* Text Testimonials */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {testimonials.filter(t => t.testimonial_text && t.testimonial_text !== 'Video testimonial from demo center inauguration').map((testimonial, index) => (
              <div key={testimonial.id} className="bg-gray-50 p-6 rounded-lg shadow-lg" data-testid={`testimonial-${index}`}>
                <div className="text-[#1B3C9B] text-4xl mb-4">"</div>
                <p className="text-gray-700 mb-4 italic">{testimonial.testimonial_text}</p>
                <div className="border-t pt-4">
                  <p className="font-semibold text-gray-900">{testimonial.client_name}</p>
                  {testimonial.company_name && (
                    <p className="text-sm text-gray-600">{testimonial.company_name}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Client Logos Section */}
      <section className="py-16 bg-gray-50" data-testid="clients-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Valued Clients</h2>
            <div className="w-24 h-1 bg-blue-900 mx-auto mb-6"></div>
            <p className="text-lg text-gray-700">Trusted by over 2000+ leading organizations</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center">
            {clientLogos.map((client, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition flex items-center justify-center" data-testid={`client-logo-${index}`}>
                <img src={client.src} alt={client.name} className="max-h-16 w-auto grayscale hover:grayscale-0 transition" />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-16 bg-gradient-to-br from-[#1B3C9B] to-[#2046A4] text-white" data-testid="contact-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Get In Touch</h2>
            <div className="w-24 h-1 bg-white mx-auto mb-6"></div>
            <p className="text-xl text-blue-100">One passion, One Goal - Let's work together!</p>
          </div>
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-bold mb-6">Contact Information</h3>
              <div className="space-y-4">
                <div className="flex items-start">
                  <MapPin className="w-6 h-6 mr-4 mt-1 flex-shrink-0" />
                  <div>
                    <p className="font-semibold">Address</p>
                    <p className="text-blue-100">Accurex Solutions Pvt. Ltd.<br />Bengaluru, Karnataka, India</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <Phone className="w-6 h-6 mr-4 mt-1 flex-shrink-0" />
                  <div>
                    <p className="font-semibold">Phone</p>
                    <p className="text-blue-100">24x7 Support Available</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <Mail className="w-6 h-6 mr-4 mt-1 flex-shrink-0" />
                  <div>
                    <p className="font-semibold">Email</p>
                    <p className="text-blue-100">info@accurexsolutions.com</p>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <form onSubmit={handleContactSubmit} className="space-y-4" data-testid="contact-form">
                <div>
                  <input
                    type="text"
                    placeholder="Your Name *"
                    required
                    value={contactForm.name}
                    onChange={(e) => setContactForm({...contactForm, name: e.target.value})}
                    className="w-full px-4 py-3 rounded-lg text-gray-900"
                    data-testid="contact-name"
                  />
                </div>
                <div>
                  <input
                    type="email"
                    placeholder="Your Email *"
                    required
                    value={contactForm.email}
                    onChange={(e) => setContactForm({...contactForm, email: e.target.value})}
                    className="w-full px-4 py-3 rounded-lg text-gray-900"
                    data-testid="contact-email"
                  />
                </div>
                <div>
                  <input
                    type="tel"
                    placeholder="Phone Number"
                    value={contactForm.phone}
                    onChange={(e) => setContactForm({...contactForm, phone: e.target.value})}
                    className="w-full px-4 py-3 rounded-lg text-gray-900"
                    data-testid="contact-phone"
                  />
                </div>
                <div>
                  <input
                    type="text"
                    placeholder="Company Name"
                    value={contactForm.company}
                    onChange={(e) => setContactForm({...contactForm, company: e.target.value})}
                    className="w-full px-4 py-3 rounded-lg text-gray-900"
                    data-testid="contact-company"
                  />
                </div>
                <div>
                  <textarea
                    placeholder="Your Message *"
                    required
                    rows="4"
                    value={contactForm.message}
                    onChange={(e) => setContactForm({...contactForm, message: e.target.value})}
                    className="w-full px-4 py-3 rounded-lg text-gray-900"
                    data-testid="contact-message"
                  ></textarea>
                </div>
                <button
                  type="submit"
                  disabled={submitStatus === 'sending'}
                  className="w-full bg-yellow-400 text-blue-900 px-8 py-3 rounded-lg font-semibold hover:bg-yellow-300 transition disabled:opacity-50"
                  data-testid="contact-submit"
                >
                  {submitStatus === 'sending' ? 'Sending...' : 'Send Message'}
                </button>
                {submitStatus === 'success' && (
                  <p className="text-green-400 text-center">Message sent successfully!</p>
                )}
                {submitStatus === 'error' && (
                  <p className="text-red-400 text-center">Error sending message. Please try again.</p>
                )}
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8" data-testid="footer">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400">
            © 1987 - 2025. Accurex Solutions Pvt. Ltd. | 39 Years of Industry Experience | Trusted Partner in Electronics Manufacturing
          </p>
          <p className="text-sm text-gray-500 mt-2">
            <strong>Keywords:</strong> SMT Equipment India | PCB Assembly Solutions | Semiconductor Testing | Automatic Test Equipment | Electronic Manufacturing Services | Pick and Place Machines | Reflow Ovens | X-Ray Inspection | AOI Systems | Capital Equipment
          </p>
        </div>
      </footer>

      {/* Product Details Modal */}
      {selectedCategory && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={closeProductModal}>
          <div className="bg-white rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="bg-gradient-to-r from-[#1B3C9B] to-[#2046A4] text-white p-6 flex justify-between items-center">
              <div>
                <h2 className="text-3xl font-bold mb-2">{selectedCategory}</h2>
                <p className="text-blue-100">{categoryProducts.length} Products Available</p>
              </div>
              <button onClick={closeProductModal} className="text-white hover:bg-white/20 rounded-full p-2 transition">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="overflow-y-auto max-h-[calc(90vh-120px)] p-6">
              <div className="grid md:grid-cols-2 gap-6">
                {categoryProducts.map((product, index) => (
                  <div key={product.id} className="bg-gray-50 rounded-lg p-6 border-2 border-gray-200 hover:border-[#1B3C9B] hover:shadow-lg transition">
                    <div className="flex justify-between items-start mb-3">
                      {product.is_featured && (
                        <div className="inline-block bg-white text-[#1B3C9B] px-3 py-1 rounded-full text-xs font-bold border-2 border-[#1B3C9B]">
                          ⭐ FEATURED
                        </div>
                      )}
                    </div>
                    <h3 className="text-xl font-bold text-[#1B3C9B] mb-2">{product.name}</h3>
                    {product.manufacturer && (
                      <div className="text-sm text-gray-700 font-semibold mb-3 bg-white px-3 py-1 rounded inline-block">
                        🏭 {product.manufacturer}
                      </div>
                    )}
                    <p className="text-gray-700 mb-4 text-sm">{product.description}</p>
                    {product.features && product.features.length > 0 && (
                      <div className="mb-4">
                        <h4 className="font-semibold text-gray-900 mb-2 text-sm">Key Features:</h4>
                        <ul className="space-y-1">
                          {product.features.slice(0, 4).map((feature, idx) => (
                            <li key={idx} className="text-xs text-gray-600 flex items-start">
                              <CheckCircle className="w-4 h-4 text-[#1B3C9B] mr-2 mt-0.5 flex-shrink-0" />
                              <span>{feature}</span>
                            </li>
                          ))}
                        </ul>
                        {product.features.length > 4 && (
                          <p className="text-xs text-gray-500 mt-2">+ {product.features.length - 4} more features</p>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
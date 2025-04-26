document.addEventListener("DOMContentLoaded", function () {
    // 1. Create glow effect element
    const glow = document.createElement("div");
    glow.id = "glow-effect";
    document.body.appendChild(glow);

    // 2. Button hover effects
    const button = document.querySelector(".glow-button");
    if (button) {
        button.addEventListener("mouseenter", function () {
            this.style.boxShadow = "0 0 20px rgba(168, 85, 247, 1), 0 0 30px rgba(147, 51, 234, 0.8)";
            this.style.transform = "scale(1.05)";
        });

        button.addEventListener("mouseleave", function () {
            this.style.boxShadow = "0 0 10px rgba(168, 85, 247, 0.8)";
            this.style.transform = "scale(1)";
        });
    }

    // 3. Perfectly aligned mouse-following glow effect
    document.addEventListener("mousemove", function (e) {
        // Directly position the glow center at mouse position
        glow.style.left = `${e.clientX}px`;
        glow.style.top = `${e.clientY}px`;

        // Update the transform to ensure perfect centering
        glow.style.transform = "translate(-50%, -50%)";
    });

    // Hide glow when mouse leaves window
    document.addEventListener("mouseout", function () {
        glow.style.opacity = "0";
    });
    document.addEventListener("mouseover", function () {
        glow.style.opacity = "1";
    });

    // CANVAS
    // 4. Enhanced floating particles effect
    const canvas = document.createElement("canvas");
    canvas.style.zIndex = "-1";
    document.body.appendChild(canvas);
    const ctx = canvas.getContext("2d");

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    class Particle {
        constructor() {
            this.reset();
            this.baseX = this.x;
            this.baseY = this.y;
            this.density = (Math.random() * 30) + 1;
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = (Math.random() * 2) + 1;
            this.color = `rgba(168, 85, 247, ${Math.random() * 0.3 + 0.1})`;
        }

        update(mouseX, mouseY) {
            // Mouse interaction
            let dx = mouseX - this.x;
            let dy = mouseY - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            let maxDistance = 100;

            if (distance < maxDistance) {
                let forceDirectionX = dx / distance;
                let forceDirectionY = dy / distance;
                let force = (maxDistance - distance) / maxDistance;
                this.x -= forceDirectionX * force * this.density * 0.6;
                this.y -= forceDirectionY * force * this.density * 0.6;
            } else {
                // Return to original position slowly
                if (Math.abs(this.x - this.baseX) > 0.5) {
                    this.x -= (this.x - this.baseX) * 0.03;
                }
                if (Math.abs(this.y - this.baseY) > 0.5) {
                    this.y -= (this.y - this.baseY) * 0.03;
                }
            }

            // Wrap around screen edges
            if (this.x < -10) this.x = canvas.width + 10;
            if (this.x > canvas.width + 10) this.x = -10;
            if (this.y < -10) this.y = canvas.height + 10;
            if (this.y > canvas.height + 10) this.y = -10;
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.closePath();
            ctx.fill();
        }
    }

    // Create particles
    const particles = [];
    const particleCount = Math.floor((canvas.width * canvas.height) / 10000);
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;

    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    // Track mouse for particles
    document.addEventListener("mousemove", function (e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Animation loop
    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw connections first (behind particles)
        drawConnections();

        // Update and draw particles
        particles.forEach(particle => {
            particle.update(mouseX, mouseY);
            particle.draw();
        });

        requestAnimationFrame(animateParticles);
    }

    function drawConnections() {
        const maxDistance = 100;
        for (let a = 0; a < particles.length; a++) {
            for (let b = a; b < particles.length; b++) {
                const dx = particles[a].x - particles[b].x;
                const dy = particles[a].y - particles[b].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < maxDistance) {
                    const opacity = 1 - (distance / maxDistance);
                    ctx.strokeStyle = `rgba(168, 85, 247, ${opacity * 0.2})`;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(particles[a].x, particles[a].y);
                    ctx.lineTo(particles[b].x, particles[b].y);
                    ctx.stroke();
                }
            }
        }
    }

    animateParticles();
});
// SCROLL
document.addEventListener('DOMContentLoaded', function () {
    const content = document.querySelector('.scrolling-content');
    const items = document.querySelectorAll('.scrolling-item');

    // İçeriği klonlayarak sürekli döngü sağla
    items.forEach(item => {
        const clone = item.cloneNode(true);
        content.appendChild(clone);
    });

    let position = 0;
    const speed = 1;
    let animationId;

    function animate() {
        position -= speed;

        // Eğer ilk öğe tamamen solun dışına çıkarsa en sona ekle
        const firstItem = content.children[0];
        if (firstItem.getBoundingClientRect().right < content.parentElement.getBoundingClientRect().left) {
            content.appendChild(firstItem);
            position += firstItem.offsetWidth; // Kayma pozisyonunu düzelt
        }

        content.style.transform = `translateX(${position}px)`;

        // Opacity efektini uygula
        Array.from(content.children).forEach(item => {
            const rect = item.getBoundingClientRect();
            const containerRect = content.parentElement.getBoundingClientRect();

            // Kenarlara yaklaştıkça opacity azalt
            if (rect.right < containerRect.left + 100 || rect.left > containerRect.right - 100) {
                item.style.opacity = "0";
            } else {
                item.style.opacity = "1";
            }
        });

        animationId = requestAnimationFrame(animate);
    }

    animate();

    // Fareyle etkileşim
    const container = document.querySelector('.scrolling-container');
    container.addEventListener('mouseenter', () => {
        cancelAnimationFrame(animationId);
    });

    container.addEventListener('mouseleave', () => {
        animate();
    });
});
// CİRCLE 
document.addEventListener('DOMContentLoaded', function () {
    // Işınların animasyon gecikmelerini ayarla
    const beams = document.querySelectorAll('.light-beam');
    beams.forEach(beam => {
        beam.style.animationDelay = `${Math.random() * 2}s`;
    });
});
// ÖDEME PLANI
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('pricing-period');
    const monthlyPrices = document.querySelectorAll('.monthly');
    const yearlyPrices = document.querySelectorAll('.yearly');

    toggle.addEventListener('change', function () {
        if (this.checked) {
            monthlyPrices.forEach(price => price.style.display = 'none');
            yearlyPrices.forEach(price => price.style.display = 'block');
        } else {
            monthlyPrices.forEach(price => price.style.display = 'block');
            yearlyPrices.forEach(price => price.style.display = 'none');
        }
    });

    // Initially hide yearly prices
    yearlyPrices.forEach(price => price.style.display = 'none');
});
// TEAM
const testimonials = {
    berkay: {
        avatar: "/static/images/berkay_gulbeyaz.jpeg",
        quote: "Geleceği yapay zekayla şekillendirmek için çalışan fütürist ve yapay zeka girişimcisi...",
    },
    mehtap: {
        avatar: "/static/images/mehtap_avci.png",
        quote: "Yapay zeka ve yazılım alanında güçlü teknik bilgiyle donanmış, yenilikçi teknoloji ürünleri geliştiren bir uzmanım. Karmaşık problemleri yaratıcı çözümlerle sadeleştirerek, geleceği şekillendiren dijital deneyimler tasarlıyorum..",
    },
    esra: {
        avatar: "/static/images/esra_isim_sahbazoglu.jpeg",
        quote: "Müşteri ihtiyaçlarına göre özel yapay zekâ çözümleri geliştiren, teknik satışla Ar-Ge arasında köprü olan uzmanım.",
    },
    nur: {
        avatar: "/static/images/nur_yalcin.jpg",
        quote: "AI temelli yenilikçi yazılım çözümleri tasarlıyor ve geliştiriyor..",
    },
    ozgur: {
        avatar: "/static/images/ozgur_cetin.jpg",
        quote: "Kurumsal yapılar için yapay zeka stratejileri geliştiren, ölçeklenebilir yazılım çözümleriyle inovasyonu yönlendiren bir liderim.",
    },
};



const buttons = document.querySelectorAll(".person-btn");
const avatar = document.getElementById("current-avatar"); // <img class="avatar-img" ...>
const testimonialText = document.getElementById("current-testimonial");

buttons.forEach((button) => {
    button.addEventListener("click", () => {
        const person = button.dataset.person;
        const data = testimonials[person];

        // Aktif butonu güncelle
        buttons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");


        // Animasyon başlat
        avatar.classList.add("slide-out");
        testimonialText.classList.add("fade-out");

        setTimeout(() => {
            avatar.src = data.avatar;
            testimonialText.textContent = data.quote;

            avatar.classList.remove("slide-out");
            avatar.classList.add("slide-in");

            testimonialText.classList.remove("fade-out");
            testimonialText.classList.add("fade-in");

            setTimeout(() => {
                avatar.classList.remove("slide-in");
                testimonialText.classList.remove("fade-in");
            }, 600);
        }, 600); // slide-out süresiyle eşleşiyor
    });
});

// RESET PASSWORD
document.addEventListener('DOMContentLoaded', function () {
    // Password Reset Form Validation
    const passwordForm = document.getElementById('password-reset-form');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function (e) {
            let isValid = true;
            const pass1 = document.getElementById('{{ form.new_password1.id_for_label }}');
            const pass2 = document.getElementById('{{ form.new_password2.id_for_label }}');

            // Clear previous errors
            document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

            // Password validation
            if (pass1.value.length < 8) {
                pass1.classList.add('is-invalid');
                document.querySelector('.password-feedback-1').textContent = 'Şifre en az 8 karakter olmalıdır.';
                isValid = false;
            }

            if (pass1.value !== pass2.value) {
                pass2.classList.add('is-invalid');
                document.querySelector('.password-feedback-2').textContent = 'Şifreler eşleşmiyor.';
                isValid = false;
            }

            if (!isValid) e.preventDefault();
        });
    }

    // Email Form Validation
    const emailForm = document.getElementById('password-reset-request-form');
    if (emailForm) {
        emailForm.addEventListener('submit', function (e) {
            const email = document.getElementById('{{ form.email.id_for_label }}');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailRegex.test(email.value)) {
                email.classList.add('is-invalid');
                document.querySelector('.email-feedback').textContent = 'Geçerli bir e-posta adresi girin.';
                e.preventDefault();
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {

    let msgType = "{{ message.tags }}";
    if (msgType === "danger") msgType = "error";  // Toastr'a uygun hale getir

    toastr.options = {
        "closeButton": true,
        "progressBar": true,
        "positionClass": "toast-top-center",
        "timeOut": "5000"
    };
    toastr[msgType]("{{ message|escapejs }}");

});
setTimeout(function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.classList.add('fade-out');
        setTimeout(() => alert.remove(), 1000);
    });
}, 4000);  // 4 saniye sonra kaybolur

// MODAL
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modelModal");
    const modalTitle = document.getElementById("modal-title");
    const modalDescription = document.getElementById("modal-description");
    const closeButton = document.querySelector(".close-button");

    document.querySelectorAll('.model-card').forEach((card, index) => {
        card.addEventListener('click', () => {
            // Örnek başlık ve açıklama atamaları (her karta özel içerik verebilirsin)
            const titles = [
                "Text to Image", "Image to Video", "Text Summarizer", "Image Enhancer",
                "Voice Cloner", "Chatbot AI", "Object Detector", "Video Generator",
                "Language Translator", "Face Recognition", "Document Scanner", "AIzmir Assistant"
            ];
            const descriptions = [
                "Yazdığınız metni yüksek kaliteli görsellere dönüştürür.",
                "Bir resmi temel alarak kısa videolar oluşturur.",
                "Uzun metinleri birkaç cümlede özetler.",
                "Görüntü kalitesini yapay zeka ile artırır.",
                "Sesinizi birebir taklit eden model.",
                "Soru-cevap, bilgi ve diyalog odaklı AI chatbot.",
                "Görüntülerdeki nesneleri tanır ve sınıflandırır.",
                "Metinden otomatik video üretimi.",
                "Gerçek zamanlı çok dilli çeviri.",
                "Yüz tanıma ve kimlik doğrulama sistemi.",
                "Belgeleri tarar, netleştirir ve OCR yapar.",
                "AIzmir’e özel dijital asistan teknolojisi."
            ];

            modalTitle.textContent = titles[index] || "Model Başlığı";
            modalDescription.textContent = descriptions[index] || "Bu modele ait detaylı açıklama buraya gelecek.";
            modal.style.display = "flex"; // veya "block" stilin nasıl tanımlandığına göre
        });
    });

    closeButton.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});

// Rubicón EAS — Schema.org JSON-LD generator
// Reads from data-page and injects appropriate @type based on URL.

(function () {
  'use strict';

  const SITE = {
    name: 'Rubicón EAS',
    legalName: 'Rubicón Empresa por Acciones Simplificadas',
    url: 'https://rubiconeas.com.py',
    phone: '+595-21-123-456',
    email: 'contacto@rubiconeas.com.py',
    address: {
      street: 'Av. Mariscal López 1234, Piso 8 Of. 803',
      city: 'Asunción',
      region: 'Central',
      country: 'PY',
    },
    geo: { lat: -25.2637, lng: -57.5759 },
    social: ['https://linkedin.com/in/juan-perez-rubicon']
  };

  const PERSON = {
    name: 'Dr. Juan María Pérez González',
    jobTitle: 'Socio Fundador · Abogado',
    url: 'https://rubiconeas.com.py/nosotros',
    alumni: [
      'Universidad Nacional de Asunción',
      'Universidad de Salamanca'
    ],
    knowsLanguage: ['es', 'en', 'pt'],
    memberOf: [
      'Colegio de Abogados del Paraguay',
      'Asociación de Abogados del Paraguay'
    ],
    award: 'Matrícula CSJ N° 23.456 · Colegio de Abogados N° 8.921'
  };

  const CSJ = 'Matrícula CSJ N° 23.456';

  function canonicalUrl() {
    return window.location.origin + window.location.pathname.replace(/\/$/, '');
  }

  function legalServiceSchema() {
    return {
      '@context': 'https://schema.org',
      '@type': 'LegalService',
      '@id': SITE.url + '#legal',
      name: SITE.name,
      alternateName: SITE.legalName,
      url: SITE.url,
      telephone: SITE.phone,
      email: SITE.email,
      image: SITE.url + '/og/og-home.png',
      logo: SITE.url + '/og/logo.svg',
      description: 'Asesoría jurídica en Paraguay. Civil, Penal y Ambiental. Matrícula CSJ 23.456. Respuesta en menos de 24 horas.',
      areaServed: [
        { '@type': 'Place', name: 'Asunción' },
        { '@type': 'Place', name: 'Central' },
        { '@type': 'Place', name: 'Alto Paraná' },
        { '@type': 'Place', name: 'Itapúa' },
      ],
      address: {
        '@type': 'PostalAddress',
        streetAddress: SITE.address.street,
        addressLocality: SITE.address.city,
        addressRegion: SITE.address.region,
        addressCountry: SITE.address.country,
      },
      geo: {
        '@type': 'GeoCoordinates',
        latitude: SITE.geo.lat,
        longitude: SITE.geo.lng,
      },
      openingHoursSpecification: [
        {
          '@type': 'OpeningHoursSpecification',
          dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
          opens: '09:00',
          closes: '18:00',
        },
        {
          '@type': 'OpeningHoursSpecification',
          dayOfWeek: ['Saturday'],
          opens: '09:00',
          closes: '12:00',
        }
      ],
      priceRange: 'Gs. 150,000 - Gs. 25,000,000',
      knowsLanguage: ['Spanish', 'English', 'Portuguese'],
      member: {
        '@type': 'Person',
        name: PERSON.name,
        jobTitle: PERSON.jobTitle,
      },
      award: CSJ,
      sameAs: SITE.social,
    };
  }

  function personSchema() {
    return {
      '@context': 'https://schema.org',
      '@type': 'Person',
      '@id': SITE.url + '#person',
      name: PERSON.name,
      jobTitle: PERSON.jobTitle,
      url: SITE.url,
      alumniOf: PERSON.alumni.map(function (name) {
        return { '@type': 'EducationalOrganization', name: name };
      }),
      knowsLanguage: PERSON.knowsLanguage,
      memberOf: PERSON.memberOf.map(function (name) {
        return { '@type': 'Organization', name: name };
      }),
      award: PERSON.award,
      worksFor: {
        '@type': 'LegalService',
        name: SITE.name,
        address: SITE.address,
      },
    };
  }

  function breadcrumbSchema(items) {
    return {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: items.map(function (item, i) {
        return {
          '@type': 'ListItem',
          position: i + 1,
          name: item.name,
          item: item.url,
        };
      }),
    };
  }

  function faqSchema(pairs) {
    return {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: pairs.map(function (p) {
        return {
          '@type': 'Question',
          name: p.q,
          acceptedAnswer: {
            '@type': 'Answer',
            text: p.a,
          },
        };
      }),
    };
  }

  function legalCaseSchema(c) {
    return {
      '@context': 'https://schema.org',
      '@type': 'LegalCase',
      name: c.title,
      description: c.summary,
      dateModified: c.year + '-12-31',
      outcome: c.outcome,
      jurisdiction: {
        '@type': 'Place',
        name: c.jurisdiction,
      },
      provider: {
        '@type': 'Attorney',
        name: PERSON.name,
      },
    };
  }

  function injectSchema(data) {
    var existing = document.querySelector('script[data-schema="dynamic"]');
    if (existing) existing.remove();
    var script = document.createElement('script');
    script.type = 'application/ld+json';
    script.dataset.schema = 'dynamic';
    script.textContent = JSON.stringify(data);
    document.head.appendChild(script);
  }

  function injectMultiSchema(arr) {
    arr.forEach(injectSchema);
  }

  // Detect page type and inject
  var path = window.location.pathname;
  var baseSchemas = [legalServiceSchema(), personSchema()];

  if (path === '/' || path === '/index.html') {
    // Home: LegalService + Person + Breadcrumb
    injectMultiSchema(baseSchemas);
    injectSchema(breadcrumbSchema([
      { name: 'Inicio', url: SITE.url + '/' },
      { name: 'Áreas de práctica', url: SITE.url + '/#areas' },
      { name: 'Contacto', url: SITE.url + '/contacto.html' },
    ]));
  } else if (path.includes('/derecho-civil')) {
    injectMultiSchema(baseSchemas);
    injectSchema({
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      name: 'Derecho Civil · Rubicón EAS',
      description: 'Servicios jurídicos en Derecho Civil: contratos, sucesiones, responsabilidad civil, propiedad y litigios.',
      about: 'Derecho Civil',
      isPartOf: { '@type': 'WebSite', name: SITE.name, url: SITE.url },
    });
  } else if (path.includes('/derecho-penal')) {
    injectMultiSchema(baseSchemas);
    injectSchema({
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      name: 'Derecho Penal · Rubicón EAS',
      description: 'Defensa penal estratégica en Paraguay. Delitos económicos, funcionarios y comunes.',
      about: 'Derecho Penal',
      isPartOf: { '@type': 'WebSite', name: SITE.name, url: SITE.url },
    });
  } else if (path.includes('/derecho-ambiental')) {
    injectMultiSchema(baseSchemas);
    injectSchema({
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      name: 'Derecho Ambiental · Rubicón EAS',
      description: 'Asesoramiento en Derecho Ambiental: infracciones, EIA, recursos naturales.',
      about: 'Derecho Ambiental',
      isPartOf: { '@type': 'WebSite', name: SITE.name, url: SITE.url },
    });
  } else if (path.includes('/nosotros')) {
    injectMultiSchema(baseSchemas);
  } else if (path.includes('/contacto')) {
    injectMultiSchema(baseSchemas);
    injectSchema({
      '@context': 'https://schema.org',
      '@type': 'ContactPage',
      name: 'Contacto · Rubicón EAS',
      description: 'Contacte a Rubicón EAS. Atención al cliente, WhatsApp institucional, formulario de consulta.',
      isPartOf: { '@type': 'WebSite', name: SITE.name, url: SITE.url },
    });
  } else if (path.includes('/casos')) {
    injectMultiSchema(baseSchemas);
  } else if (path.includes('/blog')) {
    injectMultiSchema(baseSchemas);
    injectSchema({
      '@context': 'https://schema.org',
      '@type': 'Blog',
      name: 'Artículos · Rubicón EAS',
      isPartOf: { '@type': 'WebSite', name: SITE.name, url: SITE.url },
    });
  } else {
    injectMultiSchema(baseSchemas);
  }

  // Expose globally for other scripts
  window.RUBICON_SCHEMA = {
    legalService: legalServiceSchema,
    person: personSchema,
    breadcrumb: breadcrumbSchema,
    faq: faqSchema,
    legalCase: legalCaseSchema,
    inject: injectSchema,
    injectMulti: injectMultiSchema,
  };
})();

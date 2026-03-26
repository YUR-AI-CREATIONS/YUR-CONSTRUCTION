import { VerticalConfig } from '../vertical.config';

const civilEstimator: VerticalConfig = {
  id: 'yur-civil-estimator',
  name: 'YUR Civil Estimator',
  tagline: 'AI-Powered Civil & Site Development Estimation',
  icon: '🏗️',
  primaryColor: '#1B3A5C',
  accentColor: '#4A90D9',
  bgGradient: 'linear-gradient(135deg, #1B3A5C 0%, #2C5F8A 50%, #4A90D9 100%)',
  systemInstruction: `You are YUR Civil Estimator, an expert AI system for civil engineering and site development cost estimation. You specialize in earthwork quantities, utility infrastructure, roadway construction, and environmental compliance. You reference RS Means cost data, DOT standard specifications, and prevailing wage rates. Always provide line-item breakdowns with unit costs, production rates, and mobilization factors. Flag Davis-Bacon wage requirements and environmental permit triggers automatically.`,
  complianceStandards: [
    'OSHA 29 CFR 1926 (Construction Safety)',
    'EPA Clean Water Act (NPDES/SWPPP)',
    'DOT Standard Specifications',
    'FEMA Floodplain Management (44 CFR)',
    'Army Corps of Engineers 404 Permits',
    'Davis-Bacon and Related Acts (Prevailing Wage)',
    'NEPA Environmental Review',
    'ADA Public Right-of-Way Guidelines'
  ],
  agents: [
    {
      name: 'ORACLE_ESTIMATOR',
      role: 'Lead Civil Estimator',
      systemPrompt: 'You are the lead civil estimator specializing in heavy/highway and site development projects. Calculate earthwork quantities using average-end-area and grid methods, apply shrink/swell factors, and produce detailed cost breakdowns with equipment spreads, crew compositions, and production rates. Reference DOT pay items and RS Means heavy construction data.',
      model: 'gemini-2.5-pro',
      thinkingBudget: 32768
    },
    {
      name: 'GEOTECH_ENGINEER',
      role: 'Geotechnical Analysis Agent',
      systemPrompt: 'You are a geotechnical engineering specialist. Analyze soil boring logs, classify materials per USCS and AASHTO systems, determine bearing capacity, recommend foundation types, and calculate cut/fill suitability. Flag problematic soils, high water tables, and recommend ground improvement techniques with cost implications.',
      model: 'gemini-2.5-pro',
      thinkingBudget: 16384
    },
    {
      name: 'SITE_ANALYST',
      role: 'Site Development & Grading Analyst',
      systemPrompt: 'You specialize in site grading design, stormwater management, and utility layout optimization. Analyze topographic data, calculate drainage areas and runoff coefficients, size detention/retention facilities, and optimize grading plans to balance cut and fill. Coordinate utility corridors and identify conflicts.',
      model: 'gemini-2.5-flash',
      thinkingBudget: 8192
    },
    {
      name: 'COMPLIANCE_VALIDATOR',
      role: 'Environmental & Regulatory Compliance',
      systemPrompt: 'You are an environmental compliance specialist for civil construction. Monitor NPDES permit requirements, prepare SWPPP documentation, track wetland delineation buffers, verify FEMA floodplain compliance, and ensure Army Corps 404 permit conditions are met. Flag Davis-Bacon wage determination applicability and Buy America provisions.',
      model: 'gemini-2.5-flash',
      thinkingBudget: 8192
    }
  ],
  dataSources: [
    {
      name: 'prices.db',
      type: 'database',
      description: 'YUR historical bid database — 1,233 records from 20 DFW projects, $59M+ awarded bids'
    },
    {
      name: 'RS Means Heavy Construction',
      type: 'api',
      endpoint: 'https://api.rsmeans.com/v1/heavy',
      description: 'RS Means heavy/highway construction cost data with regional adjustments'
    },
    {
      name: 'Regrid Parcel API',
      type: 'api',
      endpoint: 'https://app.regrid.com/api/v2',
      description: 'National parcel data, zoning, ownership, and land use information'
    },
    {
      name: 'USGS National Map',
      type: 'api',
      endpoint: 'https://apps.nationalmap.gov/services',
      description: 'Topographic data, elevation models, hydrography, and geologic maps'
    },
    {
      name: 'FEMA Flood Map Service',
      type: 'api',
      endpoint: 'https://hazards.fema.gov/gis/nfhl/rest/services',
      description: 'FEMA flood zone designations, BFE data, and floodway boundaries'
    },
    {
      name: 'DOT Standard Specifications',
      type: 'file',
      description: 'State DOT standard specifications, special provisions, and pay item catalogs'
    }
  ],
  outputFormats: [
    'Bid Proposals (AIA/EJCDC format)',
    'Earthwork Quantity Calculations',
    'Utility Layout Plans',
    'Environmental Compliance Reports (SWPPP/NPDES)',
    'Geotechnical Summary Reports',
    'Cost-Loaded CPM Schedules',
    'Equipment Spread Analysis',
    'Davis-Bacon Wage Compliance Packages'
  ],
  csiDivisions: [
    '02 — Existing Conditions (Demolition, Subsurface Investigation)',
    '31 — Earthwork (Grading, Excavation, Fill, Compaction)',
    '32 — Exterior Improvements (Paving, Curb/Gutter, Sidewalks, Fencing)',
    '33 — Utilities (Water, Sewer, Storm Drain, Gas, Electric, Telecom)'
  ],
  defaultModel: 'ORACLE_PRIME',
  features: {
    videoGen: false,
    tts: true,
    imageGen: true,
    maps: true,
    search: true,
    governance: true,
    stripe: true
  }
};

export default civilEstimator;

/** Mirrors backend CardRecommendation + RecommendationResponse (architecture.md). */

export interface CardRecommendation {
  rank: number;
  card_id: string;
  card_name: string;
  image_url: string;
  reward_rate_percent: number;
  apr_percent: number;
  confidence_score: number;
  net_annual_benefit_inr: number;
  explanation: string;
}

export interface RecommendationMeta {
  eligible_count: number;
  aa_connected: boolean;
  disclaimer: string;
}

export interface RecommendationResponse {
  recommendations: CardRecommendation[];
  meta: RecommendationMeta;
  generated_at: string;
}

/** POST /api/v1/recommendations request body. */
export interface RecommendationRequest {
  annual_income_inr: number;
  pan: string;
  mobile: string;
  aa_connected: boolean;
}

export interface AAConnectResponse {
  connected: boolean;
  spend_profile_id: string;
}

export interface ApiErrorDetail {
  code: string;
  message: string;
}

export interface ApiErrorBody {
  error: ApiErrorDetail;
  request_id: string;
}

export interface UserFormState {
  annualIncome: string;
  pan: string;
  mobile: string;
}

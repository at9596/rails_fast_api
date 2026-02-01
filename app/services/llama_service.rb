class LlamaService
  include HTTParty

  # Dynamic base_uri from your credentials
  base_uri Rails.application.credentials.dig(:python_api, :url) || "http://127.0.0.1:8000"

  def self.generate(prompt)
    options = {
      body: { prompt: prompt }.to_json,
      headers: { "Content-Type" => "application/json" },
      # Critical for LLMs: Increase wait time
      open_timeout: 5,
      read_timeout: 120
    }

    begin
      response = post("/generate", options)
      response.success? ? JSON.parse(response.body)["text"] : nil
    rescue Net::ReadTimeout
      Rails.logger.error "AI took too long to respond."
      nil
    rescue StandardError => e
      Rails.logger.error "LlamaService Error: #{e.message}"
      nil
    end
  end
end

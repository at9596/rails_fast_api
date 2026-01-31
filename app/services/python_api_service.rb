# app/services/python_api_service.rb
class PythonApiService
  BASE_URL = Rails.application.credentials.dig(:python_api, :url)

  def self.get_status
    response = connection.get("/compute")

    if response.success?
      JSON.parse(response.body)
    else
      offline_fallback("Error: #{response.status}")
    end
  rescue Faraday::ConnectionFailed, Faraday::TimeoutError
    offline_fallback("FastAPI Offline")
  end

  def self.process_image(image_file)
    payload = {
      file: Faraday::Multipart::FilePart.new(
        image_file.tempfile.path,
        image_file.content_type,
        image_file.original_filename
      )
    }

    response = connection.post("/process_image", payload)

    if response.success?
      { success: true, body: response.body, content_type: response.headers["content-type"] }
    else
      { success: false, error: "FastAPI Error: #{response.status}" }
    end
  rescue Faraday::ConnectionFailed, Faraday::TimeoutError => e
    { success: false, error: "Image server unreachable: #{e.message}" }
  end

  def self.analyze_csv(uploaded_file)
    payload = {
      file: Faraday::Multipart::FilePart.new(
        uploaded_file.tempfile.path,
        "text/csv",
        uploaded_file.original_filename
      )
    }

    response = connection.post("/analyze-csv", payload)

    if response.success?
      { success: true, data: JSON.parse(response.body) }
    else
      { success: false, error: "FastAPI Error: #{response.status}" }
    end
  rescue Faraday::ConnectionFailed, Faraday::TimeoutError
    { success: false, error: "Python server is unreachable." }
  end


  private

  def self.connection
    Faraday.new(url: BASE_URL) do |f|
      f.request :multipart
      f.request :url_encoded
      f.options.timeout = 2
      f.options.open_timeout = 1
      f.adapter Faraday.default_adapter
    end
  end

  def self.offline_fallback(message)
    {
      "status" => message,
      "capabilities" => [],
      "version" => "N/A",
      "environment" => "unknown"
    }
  end
end

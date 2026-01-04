module Jekyll
  module ExternalLinks
    def external_links(content)
      content.gsub(/<a([^>]*)href="(https?:\/\/[^"]+)"([^>]*)>/, '<a\1href="\2" target="_blank"\3>')
    end
  end
end

Liquid::Template.register_filter(Jekyll::ExternalLinks)
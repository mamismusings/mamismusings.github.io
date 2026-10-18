# Scheduled publishing for Mami's Musings.
#
# Each sketch in _musings/ has a  publish_on:  line in its front matter.
#   publish_on:                      -> draft, never published
#   publish_on: 2026-10-25           -> goes live 25 Oct 2026, 00:00 India time
#   publish_on: "2026-10-25 07:30"   -> goes live 25 Oct 2026, 7:30 am India time
#
# The live site (built every hour by GitHub Actions) only includes sketches
# whose time has come. Local preview (tools/preview.sh) shows everything, with
# a small "scheduled / draft" label on the ones that aren't live yet.
require "time"
require "date"

module MamisMusings
  def self.go_live(value)
    case value
    when nil, "" then nil
    when Time then value
    when Date then Time.new(value.year, value.month, value.day, 0, 0, 0)
    else Time.parse(value.to_s)
    end
  rescue ArgumentError
    Jekyll.logger.warn "Musings:", "can't read publish_on #{value.inspect} — treating as draft"
    nil
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  coll = site.collections["musings"] or next
  now = Time.now
  counts = Hash.new(0)
  coll.docs.select! do |doc|
    t = MamisMusings.go_live(doc.data["publish_on"])
    status = t.nil? ? "draft" : (t > now ? "scheduled" : "live")
    doc.data["status"] = status
    doc.data["go_live"] = t
    counts[status] += 1
    status == "live" ||
      (status == "scheduled" && site.future) ||
      (status == "draft" && site.unpublished)
  end
  Jekyll.logger.info "Musings:", "#{counts['live']} live, #{counts['scheduled']} scheduled, #{counts['draft']} draft"
end

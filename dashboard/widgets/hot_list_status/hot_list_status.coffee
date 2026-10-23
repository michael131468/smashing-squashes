class Dashing.HotListStatus extends Dashing.Widget

  constructor: ->
    super

  onData: (data) ->
    return if not @status
    status = @status.toLowerCase()

    if [ 'critical', 'warning', 'ok', 'unknown' ].indexOf(status) != -1
      backgroundClass = "hot-list-status-#{status}"
    else
      backgroundClass = "hot-list-status-unknown"

    lastClass = @lastClass

    if lastClass != backgroundClass
      $(@node).toggleClass("#{lastClass} #{backgroundClass}")
      @lastClass = backgroundClass

  ready: ->
    @onData(null)
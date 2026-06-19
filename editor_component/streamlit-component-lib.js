/**
 * Streamlit Component SDK - Lightweight Vanilla JS implementation.
 * Enables two-way communication between custom iframe components and Streamlit.
 */
(function() {
  let isReady = false;

  const Streamlit = {
    /**
     * Send a value back to Streamlit. This updates the return value
     * of the component in Python.
     */
    setComponentValue: function(value) {
      window.parent.postMessage({
        isStreamlitMessage: true,
        type: "streamlit:setComponentValue",
        value: value
      }, "*");
    },

    /**
     * Set the height of the component's iframe in Streamlit.
     */
    setFrameHeight: function(height) {
      window.parent.postMessage({
        isStreamlitMessage: true,
        type: "streamlit:setFrameHeight",
        height: height
      }, "*");
    },

    /**
     * Tell Streamlit that the component is loaded and ready to receive data.
     */
    setComponentReady: function() {
      if (!isReady) {
        window.parent.postMessage({
          isStreamlitMessage: true,
          type: "streamlit:componentReady",
          apiVersion: 1
        }, "*");
        isReady = true;
      }
    },

    /**
     * Event system for listening to updates from Python.
     */
    events: {
      addEventListener: function(type, callback) {
        window.addEventListener("message", function(event) {
          if (event.data && event.data.isStreamlitMessage) {
            if (event.data.type === "streamlit:render") {
              // Wrap detail structure to match standard CustomEvent format
              callback({
                detail: {
                  args: event.data.args,
                  disabled: event.data.disabled,
                  theme: event.data.theme
                }
              });
            }
          }
        });
      }
    },

    RENDER_EVENT: "streamlit:render"
  };

  // Expose globally
  window.Streamlit = Streamlit;
})();

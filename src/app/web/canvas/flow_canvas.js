// Canvas of the model page (M9): draws what Python sends, reports user actions as events.
// It never changes the model itself; Python writes the YAML and sends new props.
import { VueFlow, Handle } from "vueflow/vueflow.js";

export default {
  components: { VueFlow, Handle },
  props: { nodes: Array, edges: Array, readonly: Boolean, connectable: Boolean },
  template: `
    <div>
      <VueFlow :nodes="nodes" :edges="edges" :min-zoom="0.2"
               :nodes-draggable="!readonly" :nodes-connectable="connectable && !readonly"
               :edges-updatable="false" :delete-key-code="connectable && !readonly ? ['Backspace', 'Delete'] : null"
               @pane-ready="onReady" @nodes-initialized="onInitialized" @connect="onConnect" @node-drag-stop="onDragStop"
               @node-click="onClick" @edges-change="onEdgesChange">
        <template #node-default="p">
          <Handle type="target" :position="p.targetPosition" />
          <div class="rp-node-type">{{ p.data.type }}</div>
          <div class="rp-node-label">{{ p.data.label }}</div>
          <Handle type="source" :position="p.sourcePosition" />
        </template>
      </VueFlow>
    </div>`,
  methods: {
    onReady(flow) {
      this.flow = flow;
    },
    onInitialized() {
      // fit once, when the first nodes have their size; later redraws keep the user's view
      if (!this.fitted) this.fit();
      this.fitted = true;
    },
    fit() {
      if (this.flow) this.flow.fitView({ padding: 0.15 });
    },
    onConnect(c) {
      this.$emit("connect", { source: c.source, target: c.target });
    },
    onDragStop(e) {
      const n = e.node;
      this.$emit("move", { id: n.id, x: Math.round(n.position.x), y: Math.round(n.position.y) });
    },
    onClick(e) {
      this.$emit("pick", e.node.id);
    },
    onEdgesChange(changes) {
      for (const c of changes) {
        if (c.type === "remove") this.$emit("disconnect", c.id);
      }
    },
  },
};

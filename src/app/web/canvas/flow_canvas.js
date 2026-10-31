// Canvas of the model page (M9): draws what Python sends, reports user actions as events.
// It never changes the model itself; Python writes the YAML and sends new props.
import { VueFlow, Handle } from "vueflow/vueflow.js";

const TYPE = "application/x-rp-type";

export default {
  components: { VueFlow, Handle },
  props: { nodes: Array, edges: Array, palette: Array, readonly: Boolean, connectable: Boolean },
  template: `
    <div class="rp-flow">
      <div v-if="!readonly && palette && palette.length" class="rp-palette">
        <div v-for="item in palette" :key="item.type" :class="'rp-palette-item rp-' + item.type"
             draggable="true" :title="item.hint" @dragstart="onDragStart($event, item.type)"
             @click="onPaletteClick(item.type)">{{ item.label }}</div>
      </div>
      <div class="rp-flow-pane" @drop="onDrop" @dragover.prevent>
        <VueFlow :nodes="nodes" :edges="edges" :min-zoom="0.2"
                 :nodes-draggable="!readonly" :nodes-connectable="connectable && !readonly"
                 :edges-updatable="false"
                 :delete-key-code="connectable && !readonly ? ['Backspace', 'Delete'] : null"
                 @pane-ready="onReady" @nodes-initialized="onInitialized" @connect="onConnect"
                 @node-drag-stop="onDragStop" @node-click="onClick" @edge-click="onEdgeClick"
                 @edges-change="onEdgesChange">
          <template #node-default="p">
            <Handle type="target" :position="p.targetPosition" />
            <div :title="p.data.hint || null">
              <div class="rp-node-type">{{ p.data.type }}
                <span v-if="p.data.badge" class="rp-node-badge"
                      :style="p.data.tint ? { background: p.data.tint } : null">{{ p.data.badge }}</span></div>
              <div class="rp-node-label">{{ p.data.label }}</div>
            </div>
            <Handle type="source" :position="p.sourcePosition" />
          </template>
        </VueFlow>
      </div>
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
    onEdgeClick(e) {
      this.$emit("edge", e.edge.id);
    },
    onEdgesChange(changes) {
      for (const c of changes) {
        if (c.type === "remove") this.$emit("disconnect", c.id);
      }
    },
    onDragStart(ev, type) {
      ev.dataTransfer.setData(TYPE, type);
      ev.dataTransfer.effectAllowed = "copy";
    },
    dropAt(type, clientX, clientY) {
      const p = this.flow ? this.flow.screenToFlowCoordinate({ x: clientX, y: clientY }) : { x: 0, y: 0 };
      this.$emit("drop", { type, x: Math.round(p.x), y: Math.round(p.y) });
    },
    onDrop(ev) {
      const type = ev.dataTransfer.getData(TYPE);
      if (!type || this.readonly) return;
      ev.preventDefault();
      this.dropAt(type, ev.clientX, ev.clientY);
    },
    onPaletteClick(type) {
      // a click puts the node in the middle of the visible pane
      const r = this.$el.querySelector(".rp-flow-pane").getBoundingClientRect();
      this.dropAt(type, r.left + r.width / 2, r.top + r.height / 2);
    },
  },
};

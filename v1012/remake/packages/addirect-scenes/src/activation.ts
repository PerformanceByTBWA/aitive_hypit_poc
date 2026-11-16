// @ptbwa/addirect-scenes — 애디렉트 15초 광고 그래픽 장면 부품(Surface <promo:Scene>)
// - scene 값으로 장면 선택: bug · title · now · select · upload · ttal · cards · promo · band · end
// - 문구는 copy 속성(| 로 구분), 그림은 image-1~image-4(media:Image) 로 받음 — 설계도에서 바꾸면 다시 렌더
// - 구조는 Hypit 설치본 예제 semantic-composition/responsive-explainer 를 따름
import { assertAttributes, assertEmptyElement, createMarkupSurfaceFacet, textAttribute } from "@hypit/hypit/markup";
import { canonicalize, sameType } from "@hypit/hypit/protocol";
import { sealGraphFragment } from "@hypit/hypit/author";
import { createAdmissionPackageFacet } from "@hypit/hypit/admission";
import { createProducerPackageFacet } from "@hypit/hypit/producer";
import { blobTypes } from "@hypit/hypit/blob";
import type { ProducerPackage } from "@hypit/hypit/producer";
import type { AdmissionPackage } from "@hypit/hypit/admission";
import type { BlobRef, ModuleManifest, TypeRef, TypedRecord } from "@hypit/hypit/protocol";
import type { StructuredSurfaceHandler, SurfaceResolvedReference } from "@hypit/hypit/markup";
import { compositionTypes } from "@hypit/composition";
import { mediaTypes } from "@hypit/media";
import type { FontStackRef } from "@hypit/media";
import { timelineTypes } from "@hypit/timeline";
import type { Timeline } from "@hypit/timeline";
import { spatialTypes } from "@hypit/spatial";
import type { SpatialFrame } from "@hypit/spatial";
import { temporalTypes } from "@hypit/temporal";
import type { TemporalWindow } from "@hypit/temporal";
import { resolveTemporalWindowReference, temporalWindowAttributeNames, temporalWindowAttributeVocabulary,
  resolveTemporalContext, temporalContextAttributeVocabulary } from "@hypit/temporal/markup";
import { renderScene, SCENES } from "./render.js";
import type { SceneOptions } from "./render.js";

const module = { name: "@ptbwa/addirect-scenes", version: "1" } as const;
const optionsType = { module, name: "SceneOptions" };
const plain = { module, name: "compose" };
const withImages = { module, name: "compose-images" };
const IMAGE_SLOTS = ["image1", "image2", "image3", "image4"] as const;
const baseInputs = [
  { name: "timeline", type: timelineTypes.timeline }, { name: "within", type: spatialTypes.frame },
  { name: "window", type: temporalTypes.window },
  { name: "font", type: mediaTypes.fontStack }, { name: "fontHeavy", type: mediaTypes.fontStack },
  { name: "fontHand", type: mediaTypes.fontStack }, { name: "options", type: optionsType },
];
const imageInputs = [...baseInputs, ...IMAGE_SLOTS.map(name => ({ name, type: blobTypes.blob }))];
const outputs = [{ name: "visual", type: compositionTypes.visualTrack }];

export const manifest: ModuleManifest = { format: "hypit.module@1", ...module,
  dependencies: [compositionTypes.visualTrack, mediaTypes.fontStack, timelineTypes.timeline,
    spatialTypes.frame, temporalTypes.window, blobTypes.blob].map(type => ({ module: type.module })),
  types: [{ name: optionsType.name }], capabilities: [],
  producers: [{ name: plain.name, inputs: baseInputs, outputs, needs: [] },
    { name: withImages.name, inputs: imageInputs, outputs, needs: [] }],
};

function fragmentFor(producer: { module: typeof module; name: string }, inputs: typeof imageInputs) {
  return sealGraphFragment({ inputs, operations: [{ id: "compose", producer,
    inputs: Object.fromEntries(inputs.map(input => [input.name, { kind: "fragment-input" as const, name: input.name }])),
    result: { kind: "output", name: "visual" } }],
    exports: [{ name: "visual", type: compositionTypes.visualTrack, root: { kind: "fragment-operation", operation: "compose" } }],
  });
}
const plainFragment = fragmentFor(plain, baseInputs);
const imageFragment = fragmentFor(withImages, imageInputs);

const inline = <T>(record: { value: { kind: string; value?: unknown } } | undefined): T => {
  if (record?.value.kind !== "inline") throw new Error("Scene inputs must be inline values.");
  return record.value.value as T;
};
function image(record: TypedRecord | undefined): BlobRef {
  if (record === undefined || record.value.kind !== "blob" || !record.value.mediaType.startsWith("image/"))
    throw new Error("Scene image inputs must be image Blob Artifacts (media:Image).");
  return record.value;
}
const handler = (images: boolean) => ({ inputs }: { inputs: Record<string, TypedRecord | undefined> }) => ({ needs: {}, outputs: {
  visual: { kind: "inline" as const, value: canonicalize(renderScene(inline<Timeline>(inputs.timeline),
    inline<SpatialFrame>(inputs.within), inline<TemporalWindow>(inputs.window),
    { main: inline<FontStackRef>(inputs.font).faces, heavy: inline<FontStackRef>(inputs.fontHeavy).faces,
      hand: inline<FontStackRef>(inputs.fontHand).faces },
    inline<SceneOptions>(inputs.options), images ? IMAGE_SLOTS.map(slot => image(inputs[slot])) : [])) },
} });
const component: ProducerPackage & AdmissionPackage = { producers: [
  { producer: plain, handler: handler(false) }, { producer: withImages, handler: handler(true) }] } as unknown as ProducerPackage & AdmissionPackage;

const IMAGE_ATTRS = ["image-1", "image-2", "image-3", "image-4"];
export const decodeSurface: StructuredSurfaceHandler = ({ element, resolveReference }) => {
  assertAttributes(element, ["id", "scene", "copy", "stack-order", "timeline", "within", "font", "font-heavy", "font-hand",
    ...IMAGE_ATTRS, ...temporalWindowAttributeNames]);
  assertEmptyElement(element);
  const id = textAttribute(element, "id");
  const scene = textAttribute(element, "scene");
  if (!(SCENES as readonly string[]).includes(scene)) throw new Error(`Scene.scene must be one of ${SCENES.join(", ")}.`);
  const reference = (name: string, type: TypeRef): SurfaceResolvedReference => {
    const raw = element.attributes[name];
    if (typeof raw !== "object" || raw.kind !== "reference") throw new Error(`${name} must be a reference.`);
    const value = resolveReference(raw.path);
    if (value === undefined || !sameType(type, value.type)) throw new Error(`${name} has the wrong type.`);
    return value;
  };
  const context = resolveTemporalContext({ element, resolveReference });
  const window = resolveTemporalWindowReference({ element, resolveReference });
  const present = IMAGE_ATTRS.filter(name => element.attributes[name] !== undefined);
  if (present.length !== 0 && present.length !== IMAGE_ATTRS.length) throw new Error("Scene takes all four image-N attributes or none.");
  const images = present.length === IMAGE_ATTRS.length;
  const options: SceneOptions = { id, scene: scene as SceneOptions["scene"], stackOrder: Number(textAttribute(element, "stack-order")),
    copy: textAttribute(element, "copy").split("|").map(part => part.trim()) };
  const fragment = images ? imageFragment : plainFragment;
  const inputs: Record<string, unknown> = { timeline: context.timeline.ref, within: reference("within", spatialTypes.frame).ref,
    window: window.ref, font: reference("font", mediaTypes.fontStack).ref, fontHeavy: reference("font-heavy", mediaTypes.fontStack).ref,
    fontHand: reference("font-hand", mediaTypes.fontStack).ref, options: { kind: "record", id: `${id}.options` } };
  if (images) IMAGE_SLOTS.forEach((slot, i) => { inputs[slot] = reference(IMAGE_ATTRS[i]!, blobTypes.blob).ref; });
  return { records: [{ id: `${id}.options`, type: optionsType, value: { kind: "inline", value: canonicalize(options) }, range: element.range }],
    fragments: [fragment],
    components: [{ id, fragment: fragment.id, inputs, outputs: { visual: `${id}.visual` }, range: element.range }],
    exports: [`${id}.visual`] } as unknown as ReturnType<StructuredSurfaceHandler>;
};

const declaration = { name: "scene", tag: "Scene", mode: "structured" as const,
  outputs: [compositionTypes.visualTrack, optionsType],
  vocabulary: { summary: "애디렉트 15초 광고의 그래픽 장면 하나(scene 으로 선택, copy 로 문구, image-1~4 로 그림).",
    attributes: [
      ...["id", "scene", "copy", "stack-order"].map(name => ({ name, kind: "literal" as const, required: true, summary: name })),
      ...temporalContextAttributeVocabulary,
      ...[{ name: "within", type: spatialTypes.frame }, { name: "font", type: mediaTypes.fontStack },
        { name: "font-heavy", type: mediaTypes.fontStack }, { name: "font-hand", type: mediaTypes.fontStack }]
        .map(({ name, type }) => ({ name, kind: "reference" as const, required: true, accepts: [type], summary: name })),
      ...IMAGE_ATTRS.map(name => ({ name, kind: "reference" as const, required: false, accepts: [blobTypes.blob], summary: name })),
      ...temporalWindowAttributeVocabulary,
    ], ports: [{ name: "visual", type: compositionTypes.visualTrack, summary: "그래픽 장면 VisualTrack" }],
    example: '<promo:Scene id="title" scene="title" copy="모두의 TV광고|애디렉트" stack-order="40" timeline={speech.timeline} within={wide.bounds} font={kr} font-heavy={kr-heavy} font-hand={hand} during={speech.title}/>',
  },
};
export const hypitPackage = { format: "hypit.package@1" as const, modules: [{ manifest }],
  facets: [createProducerPackageFacet(component), createAdmissionPackageFacet(component),
    createMarkupSurfaceFacet({ module, declaration, handler: decodeSurface })] };
export default hypitPackage;

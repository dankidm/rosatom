<script lang="ts">
	import { open } from "@tauri-apps/plugin-dialog";
	import { convertFileSrc } from "@tauri-apps/api/core";
	import { onMount } from "svelte";
	import { crossfade, fade } from "svelte/transition";

	import type { Point, UploadResponse } from "$lib/types";
	import {
		IsPointInPolygon,
		PolygonToSVGPath,
		TransformPolygon,
	} from "$lib/helpers";
	import { ConvertImgToBase64, GetSegments } from "$lib/integrations";
	import { fetch } from "@tauri-apps/plugin-http";
	import Loader from "$lib/components/Loader.svelte";
	import Confirm from "$lib/components/Confirm.svelte";

	export const UploadImageToServer = async (base64string: string) => {
		let res = await fetch("http://localhost:5000", {
			method: "POST",
			body: JSON.stringify({
				image: base64string,
			}),
			headers: {
				"Content-Type": "application/json",
			},
		});

		if (!res.ok) {
			return {
				image_hash: "",
				message: res.statusText,
			};
		}

		return (await res.json()) as UploadResponse;
	};

	let loadedImage: HTMLImageElement | undefined = $state(undefined);

	let imgWidth = $state(0);
	let imgHeight = $state(0);
	let imgSrc = $state("");
	let imgPath = $state("");

	let confirmed = $state(false);

	let polygons: Point[][] = $state([]);

	const polyDefaultColor = "#cc00cc50";
	const polyHoverColor = "#ff000050";
	const polyReferenceColor = "#0000ff50";
	const polySelectedColor = "#00ff0050";

	let hoveredPolyIndex = $state(-1);
	let referencePolyIndex = $state(-1);

	const DeterminePolyColor = (index: number) => {
		if (index == referencePolyIndex) {
			return polyReferenceColor;
		}

		if (index == hoveredPolyIndex) {
			return polyHoverColor;
		}

		return polyDefaultColor;
	};

	let container: HTMLDivElement | undefined = $state(undefined);

	const openImage = async () => {
		const file = await open({
			multiple: false,
			directory: false,
		});

		if (file != null) {
			imgSrc = convertFileSrc(file);
			imgPath = file;
		}

		confirmed = false;
		polygons = [];
		DOMPolygons = [];
	};

	const GetHoveredPolygon = (e: MouseEvent) => {
		if (loadedImage) {
			let mousePos: Point = {
				x: e.clientX,
				y: e.clientY,
			};

			for (let i = 0; i < DOMPolygons.length; i++) {
				if (i == referencePolyIndex) {
					continue;
				}
				if (IsPointInPolygon(mousePos, DOMPolygons[i])) {
					return i;
				}
			}
		}

		return -1;
	};

	const UpdatePolygons = async () => {
		if (loadedImage) {
			let base64str = await ConvertImgToBase64(loadedImage);
			let uploadRes = await UploadImageToServer(base64str);

			if (uploadRes.image_hash != "") {
				let newPolys = await GetSegments(
					fetch(`http://localhost:5000/${uploadRes.image_hash}/segments`),
				);
				polygons = newPolys;
				DOMPolygons = UpdateDOMPolygons();
				console.log(polygons);
			} else {
				console.log(uploadRes.message);
			}
		}
	};

	let DOMPolygons: Point[][] = $state([]);

	const UpdateDOMPolygons = () => {
		let newPolys: Point[][] = [];
		if (loadedImage) {
			for (let i = 0; i < polygons.length; i++) {
				newPolys.push(
					TransformPolygon(
						polygons[i],
						loadedImage.getBoundingClientRect(),
						320,
					),
				);
			}
		}

		return newPolys;
	};

	const observer = new MutationObserver(() => {
		DOMPolygons = UpdateDOMPolygons();
	});

	onMount(() => {
		if (container) {
			observer.observe(container, {
				attributes: false,
				childList: true,
				subtree: false,
			});
		}
	});
</script>

<svelte:document
	onmousemove={(e) => {
		hoveredPolyIndex = GetHoveredPolygon(e);
	}}
	onscroll={() => {
		DOMPolygons = UpdateDOMPolygons();
	}}
/>

<svelte:window
	on:resize={() => {
		DOMPolygons = UpdateDOMPolygons();
	}}
/>

<div bind:this={container} class="container mx-auto p-4 lg:p-8 lg:text-lg">
	<h1 class="text-4xl font-black mb-4">KomIT CarPaint</h1>
	<Loader onclick={openImage} {imgPath} />
	{#if imgSrc != ""}
		<div class="grid md:grid-cols-2 xl:grid-cols-5 gap-4" transition:fade>
			<div
				class="relative rounded-xl overflow-hidden xl:col-span-2"
				onclick={() => {
					referencePolyIndex = hoveredPolyIndex;
				}}
				role="presentation"
			>
				{#each polygons as poly, i}
					<figure
						class="absolute inset-0 origin-top-left"
						style={`transform: scaleY(${loadedImage ? imgHeight / imgWidth : 1})`}
					>
						<svg
							viewBox={"0 0 320 320"}
							xmlns="http://www.w3.org/2000/svg"
							fill={DeterminePolyColor(i)}
						>
							<polygon points={PolygonToSVGPath(poly)} />
						</svg>
					</figure>
				{/each}

				<img
					bind:this={loadedImage}
					bind:naturalWidth={imgWidth}
					bind:naturalHeight={imgHeight}
					class="w-full"
					src={imgSrc}
					alt=""
				/>
			</div>
			<div class="xl:col-span-3 h-full relative">
				<div
					class="absolute inset-0 transition-opacity duration-500"
					class:opacity-0={confirmed}
					class:pointer-events-none={confirmed}
				>
					<Confirm
						confirm={() => {
							confirmed = true;
							UpdatePolygons();
						}}
						deny={() => {
							imgPath = "";
							imgSrc = "";
						}}
					/>
				</div>
				<div
					class="absolute inset-0 transition-opacity duration-500"
					class:opacity-0={!confirmed}
					class:pointer-events-none={!confirmed}
				>
					<h2 class="2xl">Выберите эталонную деталь</h2>
				</div>
			</div>
		</div>
	{/if}
</div>

<script lang="ts">
	import { fade, fly } from "svelte/transition";

	let {
		onclick,
		imgPath,
	}: { onclick: () => Promise<void> | void; imgPath: string } = $props();
</script>

<div
	class="bg-sky-50 flex flex-col mb-4 lg:text-lg
				 justify-center items-center rounded-xl
				 border-purple-200 border-dashed border-4 transition-all duration-1000"
	class:py-16={imgPath == ""}
	class:py-0={imgPath != ""}
>
	<h2
		class="text-3xl transition-all duration-500"
		style={`line-height: ${imgPath == "" ? 1 : 0}; opacity: ${imgPath == "" ? 1 : 0}`}
	>
		Загрузите изображение машины:
	</h2>
	<div class="p-4 flex w-full justify-center items-center gap-4">
		<button
			onclick={async () => {
				await onclick();
			}}
			class="bg-purple-600 text-white w-max
						 rounded-xl px-4 py-2 text-nowrap
						 shadow-purple-600/20 shadow-md transition-all
						 hover:bg-purple-500 hover:shadow-lg hover:shadow-purple-600/40"
		>
			Загрузить файл
		</button>
		<div
			class="transition-all duration-500"
			class:w-0={imgPath == ""}
			class:w-full={imgPath != ""}
		>
			<span
				class="transition-opacity delay-300 duration-500"
				class:opacity-0={imgPath == ""}>{imgPath}</span
			>
		</div>
	</div>
</div>

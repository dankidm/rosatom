<script lang="ts">
	let {
		confirm,
		deny,
	}: {
		confirm: () => Promise<void> | void;
		deny: () => Promise<void> | void;
	} = $props();
</script>

<div
	class="xl:col-span-3 h-full flex flex-col justify-center items-center p-4 gap-4"
>
	<h3 class="text-2xl text-center">Расчитать покраску для данной машины?</h3>
	<div class="flex gap-2">
		<button
			onclick={confirm}
			class="bg-purple-600 text-white
						 rounded-xl px-4 py-2
						 shadow-purple-600/20 shadow-md transition-all
						 hover:bg-purple-500 hover:shadow-lg hover:shadow-purple-600/40"
		>
			Подтвердить
		</button>
		<button
			onclick={deny}
			class="bg-red-600 text-white
						 rounded-xl px-4 py-2
						 shadow-red-600/20 shadow-md transition-all
						 hover:bg-red-500 hover:shadow-lg hover:shadow-red-600/40"
		>
			Отмена
		</button>
	</div>
</div>

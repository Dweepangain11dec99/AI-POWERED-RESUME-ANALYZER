
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	type MatcherParam<M> = M extends (param : string) => param is (infer U extends string) ? U : string;

	export interface AppTypes {
		RouteId(): "/" | "/app" | "/app/ab-test" | "/app/analyze" | "/app/cover-letter" | "/app/github" | "/app/market" | "/app/portfolio" | "/app/recruiter" | "/app/skill-gap" | "/app/timeline" | "/login";
		RouteParams(): {
			
		};
		LayoutParams(): {
			"/": Record<string, never>;
			"/app": Record<string, never>;
			"/app/ab-test": Record<string, never>;
			"/app/analyze": Record<string, never>;
			"/app/cover-letter": Record<string, never>;
			"/app/github": Record<string, never>;
			"/app/market": Record<string, never>;
			"/app/portfolio": Record<string, never>;
			"/app/recruiter": Record<string, never>;
			"/app/skill-gap": Record<string, never>;
			"/app/timeline": Record<string, never>;
			"/login": Record<string, never>
		};
		Pathname(): "/" | "/app" | "/app/ab-test" | "/app/analyze" | "/app/cover-letter" | "/app/github" | "/app/market" | "/app/portfolio" | "/app/recruiter" | "/app/skill-gap" | "/app/timeline" | "/login";
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): "/favicon.svg" | string & {};
	}
}
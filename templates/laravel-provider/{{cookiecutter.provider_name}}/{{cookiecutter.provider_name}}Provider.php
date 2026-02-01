<?php

namespace Inovector\Mixpost\SocialProviders\{{ cookiecutter.provider_name }};

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Inovector\Mixpost\Abstracts\SocialProvider;
use Inovector\Mixpost\Http\Resources\AccountResource;
use Inovector\Mixpost\SocialProviders\{{ cookiecutter.provider_name }}\Concerns\ManagesOAuth;
use Inovector\Mixpost\SocialProviders\{{ cookiecutter.provider_name }}\Concerns\ManagesResources;
use Inovector\Mixpost\Support\SocialProviderPostConfigs;

class {{ cookiecutter.provider_name }}Provider extends SocialProvider
{
    use ManagesOAuth;
    use ManagesResources;

    public array $callbackResponseKeys = ['code', 'state'];

    protected string $apiBaseUrl = '{{ cookiecutter.api_base_url }}';
    protected string $oauthBaseUrl = '{{ cookiecutter.oauth_base_url }}';
    protected string $tokenUrl = '{{ cookiecutter.token_url }}';

    public static function name(): string
    {
        return '{{ cookiecutter.provider_name }}';
    }

    public static function service(): string
    {
        return \Inovector\Mixpost\Services\{{ cookiecutter.provider_name }}Service::class;
    }

    public static function postConfigs(): SocialProviderPostConfigs
    {
        return SocialProviderPostConfigs::make()
            ->simultaneousPosting({{ cookiecutter.supports_scheduling }})
            ->minTextChar(1)
            ->maxTextChar({{ cookiecutter.max_text_char }})
            ->minPhotos(0)
            ->maxPhotos({{ cookiecutter.max_photos }})
            ->minVideos(0)
            ->maxVideos({{ cookiecutter.max_videos }})
            ->minGifs(0)
            ->maxGifs(1)
            ->allowMixingMediaTypes(false);
    }

    public static function externalPostUrl(AccountResource $accountResource): string
    {
        $postId = $accountResource->pivot->provider_post_id ?? '';
        return "https://example.com/post/{$postId}";
    }

    /**
     * Make authenticated API request
     */
    protected function apiRequest(string $method, string $endpoint, array $params = [], array $body = []): array
    {
        $token = $this->getAccessToken();

        $url = "{$this->apiBaseUrl}/{$endpoint}";
        if (!empty($params)) {
            $url .= '?' . http_build_query($params);
        }

        $request = Http::withHeaders([
            'Authorization' => "Bearer {$token['access_token']}",
            'Content-Type' => 'application/json',
        ]);

        $response = empty($body) 
            ? $request->{$method}($url)
            : $request->{$method}($url, $body);

        return $response->json() ?? [];
    }

    /**
     * Get current user info
     */
    public function getUser(): array
    {
        return $this->apiRequest('get', 'me');
    }

    /**
     * Publish post
     */
    public function publishPost(string $text, array $options = []): array
    {
        $result = $this->apiRequest('post', 'posts', [], [
            'content' => $text,
            'media' => $options['media'] ?? [],
        ]);

        if (isset($result['id'])) {
            return $this->response(static::RESPONSE_SUCCESS, [
                'id' => $result['id'],
            ]);
        }

        return $this->response(static::RESPONSE_ERROR, $result);
    }
}

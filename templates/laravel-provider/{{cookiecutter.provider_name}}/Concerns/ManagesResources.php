<?php

namespace Inovector\Mixpost\SocialProviders\{{ cookiecutter.provider_name }}\Concerns;

trait ManagesResources
{
    /**
     * Get account data for storing
     */
    public function getAccount(): array
    {
        $user = $this->getUser();

        if (empty($user) || isset($user['error'])) {
            return $this->response(static::RESPONSE_ERROR, [
                'message' => $user['error'] ?? 'Could not fetch user data'
            ]);
        }

        return $this->response(static::RESPONSE_SUCCESS, [
            'id' => $user['id'],
            'name' => $user['name'] ?? $user['display_name'] ?? 'Unknown',
            'username' => $user['username'] ?? $user['id'],
            'image' => $user['avatar'] ?? $user['profile_image_url'] ?? null,
            'data' => [
                // Add provider-specific data here
            ],
        ]);
    }

    /**
     * Get entities that can be managed
     */
    public function getEntities(): array
    {
        $user = $this->getUser();

        if (empty($user)) {
            return [];
        }

        return [
            [
                'id' => $user['id'],
                'name' => $user['name'] ?? 'Account',
                'username' => $user['username'] ?? $user['id'],
                'image' => $user['avatar'] ?? null,
            ]
        ];
    }

    /**
     * Get metrics/analytics
     */
    public function getMetrics(): array
    {
        $user = $this->getUser();

        return [
            'followers' => $user['followers_count'] ?? 0,
            'following' => $user['following_count'] ?? 0,
        ];
    }

    /**
     * Delete a post
     */
    public function deletePost(string $postId): array
    {
        $response = $this->apiRequest('delete', "posts/{$postId}");

        if (empty($response) || !isset($response['error'])) {
            return $this->response(static::RESPONSE_SUCCESS, ['deleted' => true]);
        }

        return $this->response(static::RESPONSE_ERROR, $response);
    }

    /**
     * Get post details
     */
    public function getPost(string $postId): array
    {
        $post = $this->apiRequest('get', "posts/{$postId}");

        if (empty($post) || isset($post['error'])) {
            return $this->response(static::RESPONSE_ERROR, [
                'message' => $post['error'] ?? 'Post not found'
            ]);
        }

        return $this->response(static::RESPONSE_SUCCESS, $post);
    }
}
